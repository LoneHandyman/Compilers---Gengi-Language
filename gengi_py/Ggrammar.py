from collections import OrderedDict
from copy import copy
from anytree import Node
from Gtools import Rule, MemoHelper, Stack
import Gtoken
import re
import itertools

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

  def parsing_table(self, is_clean=True):
    from Gtools import remove_left_recursion, remove_left_factoring
    equiv = self if is_clean else remove_left_recursion(remove_left_factoring(copy(self)))
    table = {}
    ambigous = False
    for r in equiv.iter_productions():
      terminals = equiv.first(r.body)
      for t in terminals:
        if not equiv.is_terminal(t):
          continue
        if t == equiv.epsilon:
          f = equiv.follow(r.head)
          for ef in f:
            if (table.get((r.head, ef))):
              ls = []
              ls.append(table[(r.head, ef)])
              ls.append(r)
              table[(r.head, ef)] = ls
              ambigous = True
            else:
              table[(r.head, ef)] = r
        else:
          if (table.get((r.head, t))):
            ls = []
            ls.append(table[(r.head, t)])
            ls.append(r)
            table[(r.head, t)] = ls
            ambigous = True
          else:
            table[(r.head, t)] = r
    return (table, ambigous)


  def parse(self, tokens):
    table, ambiguous = self.parsing_table(is_clean=True)
    if ambiguous:
      raise Warning("Ambiguous self")

    error_list = []
    tokens.append(Gtoken.Token(self.eof, ""))
    curr_token = tokens.pop(0)
    stack = Stack()

    stack.put((self.eof, None))
    root = Node(self.start)
    stack.put((self.start, root))

    top_stack = stack.peek()
    while True:
      print(f"Current_word:{curr_token},  Stack:{stack.queue}")
      if top_stack[0].type == self.eof and curr_token.type == self.eof:
        if not error_list:
          return True, root, None
        else:
          return False, root, error_list

      if self.is_terminal(top_stack[0].type):
        if top_stack[0].type == curr_token.type:
          print(f"Consume input: {curr_token}")
          stack.get()
          curr_token = tokens.pop(0)
        else:
          error_list.append(f"Expected {top_stack[0].type}")
          while curr_token.type != top_stack[0].type:
            if curr_token.type == self.eof:
              return False, root, error_list
            curr_token = tokens.pop(0)
      else:
        rule = table.get((top_stack[0].type, curr_token.type))
        stack.get()
        if rule:
          print(f"Rule: {rule}")
          symbols = rule.body[::-1]
          for symbol in symbols:
            node = Node(symbol, parent=top_stack[1].type)
            if symbol != self.epsilon:
              stack.put((symbol, node))
        else:
          error_list.append(f"Unexpected character:{curr_token.type}. Expected: {self.first(top_stack[0])}")
          follow = self.follow(top_stack[0].type) + [self.eof]
          print(f"Error! Sync set: {follow}")
          while curr_token.type not in follow:
            print(f"Skipped: {curr_token.type}")
            curr_token = tokens.pop(0)
      top_stack = stack.peek()

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