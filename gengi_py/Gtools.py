from queue import LifoQueue
from anytree import RenderTree
from collections import OrderedDict
from Gtoken import Token
from copy import copy
from Ggrammar import Grammar

class Stack(LifoQueue):
  def peek(self):
    if len(self.queue) == 0:
      return None
    return self.queue[len(self.queue) - 1]

class InvalidProduction(Exception):
  def __init__(self, message, production):
    super().__init__(message)
    self.production = production

class Rule:
  def __init__(self, head, body):
    self.head = head
    self.body = body
    if not isinstance(self.body, tuple):
      raise ValueError("Body of production must be a tuple")
    if (head,) == body:
      raise InvalidProduction("Invalid production. Head is the same as body.", self)

  def __eq__(self, other):
    return self.head == other.head and self.body == other.body

  def __str__(self):
    return "{} → {}".format(self.head, ' '.join(self.body))

  def __repr__(self):
    return "Rule({}, {})".format(repr(self.head), self.body)

  def __hash__(self):
    return hash((self.head, self.body))

class MemoHelper:
  def __init__(self, seq=()):
    self.tup = tuple(seq)

  def __eq__(self, other):
    return isinstance(self, type(other))

  def __hash__(self):
    return hash(type(self))

  def __add__(self, seq=()):
    return MemoHelper(self.tup + tuple(seq))

  def __iter__(self):
    return iter(self.tup)

  def __str__(self):
    return str(self.tup)

def show_lexical_errors(tokens):
  status = True
  for token in tokens:
    if token.bad_token:
      print("\033[91m Error", token.lexeme, "bad token found.")
      status = False
  return status

def __normalize_productions(grammar):
  normalized_grammar = copy(grammar)
  for x in grammar.nonterminals:
    for p in grammar.productions[x]:
      if len(p.body) > 1:
        p.body = tuple([x for x in p.body if x != grammar.epsilon])

  return normalized_grammar


def nonterminal_ordering(grammar):
  return [x for x in grammar.nonterminals]


def __generate_key(grammar, x):
  new_x = x
  while new_x in grammar.nonterminals:
    new_x += "'"

  return new_x

def remove_immediate_left_recursion(grammar, A):
  productions = grammar.productions[A]
  recursive = []
  nonrecursive = []
  new_productions = []

  for p in productions:
    if p.is_left_recursive():
      recursive.append(p.body)
    else:
      nonrecursive.append(p.body)

  if not recursive:
      return productions

  new_A = __generate_key(grammar, A)
  for b in nonrecursive:
    new_productions.append(Rule(A, b + (new_A,)))

  for a in recursive:
    new_productions.append(Rule(new_A, a[1:] + (new_A,)))

  new_productions.append(Rule(new_A, (grammar.epsilon,)))
  return new_productions

def remove_left_recursion(g):
  temp_grammar = copy(g)
  new_grammar = Grammar(start=temp_grammar.start, epsilon=temp_grammar.epsilon, eof=temp_grammar.eof)
  nonterminals = nonterminal_ordering(temp_grammar)

  for i in range(0, len(nonterminals)):
    ai = nonterminals[i]
    for j in range(0, i):
      aj = nonterminals[j]
      for p_ai in temp_grammar.productions[ai]:
        if p_ai.body and aj == p_ai.body[0]:
          replaced_productions = [Rule(ai, p_aj.body + p_ai.body[1:]) for p_aj in temp_grammar.productions[aj]]
          can_remove_productions = any(map(lambda x: x.is_left_recursive(), replaced_productions))
          if can_remove_productions:
            temp_grammar.remove_rule(p_ai)
            for p in replaced_productions:
              temp_grammar.add_rule(p)

    new_productions = remove_immediate_left_recursion(temp_grammar, ai)
    for p in new_productions:
      new_grammar.add_rule(p)

  return __normalize_productions(new_grammar)

def check_items_equal(l):
  return l[1:] == l[:-1]


def get_max_length(lst):
  return max([len(l) for l in lst])


def get_prefixes(productions):
  common = OrderedDict()
  sorted_productions = sorted(productions)
  for x in sorted_productions:
    if x:
      common.setdefault(x[0], []).append(x)
  for k, v in common.items():
    common_index = 0
    if (len(v) > 1):
      common_index = 1
      sublist = [l[0:common_index + 1] for l in v]
      while check_items_equal(sublist) and common_index < get_max_length(v):
        common_index += 1
        sublist = [l[0:common_index + 1] for l in v]
      common_index = common_index - 1
      common[k] = [l[common_index + 1:] for l in v]
    if common_index > 0:
      common[k] = [l[common_index + 1:] for l in v]
      final_key = ' '.join(v[0][0:common_index + 1])
      common[final_key] = common[k]
      del common[k]
  return common


def check_left_factors(grammar):
  for nonterminal in grammar.nonterminals:
    productions = grammar.productions_for(nonterminal)
    if len(productions) > 1:
      first_elements = [l[0] for l in productions if l]
      result = check_items_equal(first_elements)
      diff_vals = set(first_elements)
      for i in diff_vals:
        if first_elements.count(i) > 1:
          return True
  return False


def remove_left_factoring(grammar):
  g = grammar
  while (check_left_factors(g)):
    g = __remove_left_factoring(g)
  return g


def __remove_left_factoring(grammar):
  new_grammar = Grammar(start=grammar.start, epsilon=grammar.epsilon, eof=grammar.eof)
  new_productions = []
  for nonterminal in grammar.nonterminals:
    productions = grammar.productions_for(nonterminal)
    if len(productions) > 1:
      prefixes = get_prefixes(productions)
      for prefix, v in prefixes.items():
        if (len(v) == 1):
          new_productions.append(Rule(nonterminal, tuple(v[0])))
          continue
        new_x = __generate_key(grammar, nonterminal)
        body = [prefix] + [new_x]
        new_productions.append(Rule(nonterminal, tuple(body)))
        for prod in v:
          if not prod:
            new_productions.append(Rule(new_x, tuple([grammar.epsilon])))
          else:
            new_productions.append(Rule(new_x, tuple(prod)))
    else:
        new_productions.append(Rule(nonterminal, tuple(productions[0])))

  for prod in new_productions:
      new_grammar.add_rule(prod)
  return __normalize_productions(new_grammar)


def __join_amb(entry):
  return ' | '.join([str(e) for e in entry])

def read_parsing_tree(tree):
  for pre, fill, node in RenderTree(tree):
    print(f"{pre}{node.name}")