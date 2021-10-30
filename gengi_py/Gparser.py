from Gtools import Stack
from anytree import Node
from Gtoken import Token

def parse(grammar, words):
  table = grammar.symbol_table

  error_list = []
  words.append(Token(grammar.eof, ""))
  word = words.pop(0).type
  stack = Stack()
  stack.put(grammar.eof, None)
  root = Node(grammar.start)
  stack.put((grammar.start, root))
  top_stack = stack.peek()
  if table is not None:
    while True:
      print(f"Current_word:{word},  Stack:{stack.get_body(0)}")
      if top_stack[0] == grammar.eof and word == grammar.eof:
        if not error_list:
          return True, root, []
        else:
          return False, root, error_list

      if grammar.is_terminal(top_stack[0]):
        if top_stack[0] == word:
          print(f"Consume input: {word}")
          stack.get()
          word = words.pop(0).type
        else:
          error_list.append(f"Expected {top_stack[0]}")
          while word != top_stack[0]:
            if word == grammar.eof:
              return False, root, error_list
            word = words.pop(0).type
      else:
        rule = table.get((top_stack[0], word))
        stack.get()
        if rule:
          print(f"Rule: {rule}")
          symbols = rule.body[::-1]
          for symbol in symbols:
            node = Node(symbol, parent=top_stack[1])
            if symbol != grammar.epsilon:
              stack.put((symbol, node))
        else:
          error_list.append(f"Unexpected character: {word}, Expected: {grammar.first(top_stack[0])}")
          follow = grammar.follow(top_stack[0]) + [grammar.eof]
          print(f"Error! Sync set: {follow}")
          while word not in follow:
            print(f"Skipped: {word}")
            word = words.pop(0).type
      top_stack = stack.peek()
  return False, root, []