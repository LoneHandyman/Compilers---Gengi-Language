from collections import OrderedDict
import Gtoken
import re
import itertools

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

class Grammar:
  def __init__(self, start=None, epsilon='#', eof='$'):
    self.productions = OrderedDict()
    self.start = start
    self.epsilon = epsilon
    self.eof = eof

  def remove_rule(self, rule):
    self.productions[rule.head].remove(rule)

  def is_terminal(self, s):
    return s not in self.nonterminals

  def is_start_symbol(self, symbol):
    return self.start == symbol
      
  def iter_productions(self):
    return itertools.chain.from_iterable(self.productions.values())
  
  def productions_for(self, symbol):
    return [production.body for production in self.productions[symbol]]

  @property
  def nonterminals(self):
    return self.productions.keys()

  @property
  def terminals(self):
    nonterminals = self.nonterminals
    terminals = OrderedDict()
    for r in self.iter_productions():
      for symbol in r.body:
        if symbol not in nonterminals:
          terminals.update({symbol: 1})

    return terminals.keys()

  def first_multiple(self, tokens):
    first_multiple_set = set()
    for token in tokens:
      first_set = self.first(token)
      first_multiple_set.union(first_set)
      if self.epsilon not in first_set:
        break
    return first_multiple_set

  def first(self, symbol):
    first_set = set()
    if isinstance(symbol, tuple):
      first_set = self.first_multiple(symbol)
    elif self.is_terminal(symbol):
      first_set.add(symbol)
    else:
      for production in self.productions_for(symbol):
        first_set.union(self.first(production))

    return sorted(first_set)

  def follow(self, nonterminal):
    previous = MemoHelper()
    previous += (nonterminal,)
    follow_set = set()
    if self.is_start_symbol(nonterminal):
      follow_set.add(self.eof)
    subsets = set()
    for production in self.iter_productions():
      if nonterminal in production.body:
        position = production.body.index(nonterminal)
        a = production.body[0:position]
        b = production.body[position + 1:]
        if b:
          follow_set = follow_set.union(set(self.first(b)) - {self.epsilon})
        if not b:
          subsets.add(production.head)
        elif b and self.epsilon in self.first(b):
          subsets.add(production.head)
    subsets = subsets - {nonterminal}
    for x in subsets:
      if x not in previous:
        follow_set = follow_set.union(self.follow(x, previous))
    return sorted(follow_set)

  def parse(self, tokens):
    pass

  def add_rule(self, rule):
    try:
      current_productions = self.productions[rule.head]
      if rule not in current_productions:
        current_productions.append(rule)
    except KeyError:
      self.productions[rule.head] = [rule]

def open_grammar(grammar, path):
  productions_file = open(path, 'r')
  productions_list = productions_file.readlines()
  productions_file.close()
  for rule in productions_list:
    rule = re.sub("\t\n", " ", rule)
    head, body = [item.strip() for item in rule.split('->')]
    productions = [production.strip() for production in body.split('|')]
    productions_tokenized = [tuple(production.split()) for production in productions]
    for tk_production in productions_tokenized:
      grammar.add_rule(Rule(head, tk_production))
  grammar.start = list(grammar.productions.items())[0][0]
  return grammar

grammar = Grammar()
file = open_grammar(grammar, 'GengiGrammar.gram')
#print('\u03B5')