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
      tokens_set = Gscanner.scan_code(source_code)
      grammar = Ggrammar.Grammar()
      grammar = Ggrammar.open_grammar(grammar, "GnegiGrammar.gram")
      grammar.parse(tokens_set)
    else:
      print("<Error>: The input file has not the \'gg\' extension.")
      exit(1)
  else:
    print("<Error>: Not enough arguments given.")
    exit(1)