from Gtools import show_lexical_errors, read_parsing_tree, open_grammar, pprint_table
from Gparser import parse
import Gscanner
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
      tokens_list = Gscanner.scan_code(source_code)[:-1]
      print(tokens_list)
      if show_lexical_errors(tokens_list):
        grammar = open_grammar("GengiGrammar.gram")
        parsing_table, ambiguous = grammar.parsing_table()
        pprint_table(grammar, parsing_table, padding=20)
        parsing_status, root, error_list = parse(grammar, tokens_list)
        if parsing_status:
          print("\033[32m SUCCESS:\033[37m")
          read_parsing_tree(root)
        else:
          print("\033[91m FAILURE:\033[37m")
          for error in error_list:
            print(error)
    else:
      print("<Error>: The input file has not the \'gg\' extension.")
      exit(1)
  else:
    print("<Error>: Not enough arguments given.")
    exit(1)