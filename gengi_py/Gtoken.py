token_types = ["Aritmetic_op", "Boolean_op", "Begin_braces", "End_braces",
               "Begin_brackets", "End_brackets", "Semicolon", "Comma", "Iterator_op",
               "Comparator_op", "Dot_op", "Begin_paren", "End_paren", "Id", "If", "Else",
               "Function", "Return", "Gnode", "Set", "Get", "Link", "Spawn", "Import",
               "As", "For", "While", "Sp_prep_begin", "Sp_prep_end", "Assign_op", "Number", "String", "$"]

Aritmetic_op = 0
Boolean_op = 1
Begin_braces = 2
End_braces = 3
Begin_brackets = 4
End_brackets = 5
Semicolon = 6
Comma = 7
Iterator_op = 8
Comparator_op = 9
Dot_op = 10
Begin_paren = 11
End_paren = 12
Id = 13
If = 14
Else = 15
Function = 16
Return = 17
Gnode = 18
Set = 19
Get = 20
Link = 21
Spawn = 22
Import = 23
As = 24
For = 25
While = 26
Sp_prep_begin = 27
Sp_prep_end = 28
Assign_op = 29
Number = 30
String = 31

special_single_symbols = {
  '+': token_types[Aritmetic_op], '-': token_types[Aritmetic_op], '*': token_types[Aritmetic_op],
  '/': token_types[Aritmetic_op], '^': token_types[Boolean_op], '(': token_types[Begin_paren],
  ')': token_types[End_paren], ':': token_types[Iterator_op], ';': token_types[Semicolon],
  '{': token_types[Begin_braces], '}': token_types[End_braces], '[': token_types[Begin_brackets],
  ']': token_types[End_brackets], '.': token_types[Dot_op], '%': token_types[Aritmetic_op]
}

reserved_keywords = {
  "if": token_types[If], "else": token_types[Else], "function": token_types[Function],
  "return": token_types[Return], "gnode": token_types[Gnode], "set": token_types[Set],
  "get": token_types[Get], "link": token_types[Link], "spawn": token_types[Spawn],
  "import": token_types[Import], "as": token_types[As], "for": token_types[For], 
  "while": token_types[While], "#preprocess_begin": token_types[Sp_prep_begin], 
  "#preprocess_end": token_types[Sp_prep_end]
}

class StringStream:
  def __init__(self, buffer):
    self.buffer = buffer
    self.seekp = -1
  
  def get(self):
    self.seekp += 1
    if self.seekp < len(self.buffer):
      return self.buffer[self.seekp]
    return '\0'

  def peek(self):
    peek_char = '\0'
    if self.seekp + 1 < len(self.buffer):
      peek_char = self.buffer[self.seekp + 1]
    return peek_char

  def eof(self):
    return self.seekp == len(self.buffer)

class Token:
  def __init__(self, type, lexeme, bad_token=False):
    self.type = type
    self.lexeme = lexeme
    self.bad_token = bad_token

  def __repr__(self):
    type_str = "None"
    if self.type is not None:
      type_str = self.type
    return "<Type: " + type_str + ", Lex: \'" + self.lexeme + "\' >"