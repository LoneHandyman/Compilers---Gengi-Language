from Gtools import show_lexical_errors, read_parsing_tree
import Gscanner
import Ggrammar
import sys
import os

if __name__ == '__main__':
  arguments = sys.argv
  if(len(arguments) == 2):
    r, ext = os.path.splitext(arguments[1])
    if ext == '.gg':
      source_code_file = open(arguments[1], 'r')
      source_code = source_code_file.read()
      source_code_file.close()
      tokens_list = Gscanner.scan_code(source_code)
      if show_lexical_errors(tokens_list):
        grammar = Ggrammar.Grammar()
        grammar = Ggrammar.open_grammar(grammar, "GengiGrammar.gram")
        parsing_status, root, error_list = grammar.parse(tokens_list)
        if parsing_status:
          read_parsing_tree(root)
        else:
          print(error_list)
    else:
      print("<Error>: The input file has not the \'gg\' extension.")
      exit(1)
  else:
    print("<Error>: Not enough arguments given.")
    exit(1)