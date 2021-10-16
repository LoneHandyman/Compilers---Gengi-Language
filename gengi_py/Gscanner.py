import Gtoken

def clean_code(input):
  last_got_char = ' '
  str_mode = False
  src_copy = ''
  for idx in range(0, len(input)):
    if input[idx] == 39:
      str_mode = not str_mode
    if not str_mode:
      if input[idx] == '\t' or input[idx] == '\n' or input[idx] == ' ':
        input = input[:idx] + " " + input[idx + 1:]
        if last_got_char == ' ':
          continue
    src_copy += input[idx]
    last_got_char = input[idx]
  return src_copy

def clean_comments(input):
  def kmp(source, pattern, aux):
    locations = list()
    idx_src = 0
    idx_pattern = 0

    while idx_src < len(source):
      if pattern[idx_pattern] == source[idx_src]:
        idx_pattern += 1
        idx_src += 1
      if idx_pattern == len(pattern):
        locations.append(idx_src - idx_pattern)
        idx_pattern = aux[idx_pattern - 1]

      if idx_src < len(source) and (pattern[idx_pattern] != source[idx_src]):
        if idx_pattern:
          idx_pattern = aux[idx_pattern - 1]
        else:
          idx_src += 1
    return locations

  def prefix(pattern):
    kmp_table = [0] * len(pattern)
    j = 0
    i = 1
    while i < len(pattern):
      if pattern[i] == pattern[j]:
        j += 1
        kmp_table[i] = j
        i += 1
      else:
        if j:
          j = kmp_table[j - 1]
        else:
          kmp_table[i] = 0
          i += 1
    return kmp_table
  
  merged_content = ''
  comm_pos_begin = list()
  prefix_table = prefix(">>>")
  idx = 0
  code_lines = input.splitlines()
  for idx in range(0, len(code_lines)):
    comm_pos_begin = kmp(code_lines[idx], ">>>", prefix_table)
    if len(comm_pos_begin):
      code_lines[idx] = code_lines[idx][0:comm_pos_begin[0]]
    code_lines[idx] += '\n'
    merged_content += code_lines[idx]
  return merged_content

def scan_code(input):
  tokens = list()
  free_comments_input = clean_comments(input)
  fixed_input = clean_code(free_comments_input)
  char_source = Gtoken.StringStream(fixed_input)
  while not char_source.eof():
    inflection_char = ' '
    lexeme_intent = "";
    new_token_t = None

    while inflection_char == ' ':
      inflection_char = char_source.get()
    if inflection_char.isalpha() or inflection_char == '_' or inflection_char == '#':
      lexeme_intent += inflection_char
      next_tk_char = char_source.peek()
      while not char_source.eof() and (next_tk_char.isalnum() or next_tk_char == '_'):
        lexeme_intent += next_tk_char
        char_source.get()
        next_tk_char = char_source.peek()
      if not char_source.eof():
        if lexeme_intent in Gtoken.reserved_keywords:
          new_token_t = Gtoken.reserved_keywords[lexeme_intent]
        else:
          good_id = True;
          for c in lexeme_intent:
            if c != '_' and not c.isalnum:
              good_id = False
              break
          if good_id:
            new_token_t = Gtoken.token_types[Gtoken.Id]
    elif inflection_char.isdigit() or ((inflection_char == '.' or inflection_char == '-') and char_source.peek().isdigit()):
      next_tk_char = char_source.peek()
      if inflection_char != '-':
        lexeme_intent += inflection_char
      while not char_source.eof() and (next_tk_char.isdigit() or next_tk_char == '.'):
        lexeme_intent += next_tk_char
        char_source.get()
        next_tk_char = char_source.peek()
      if not char_source.eof():
        dot_count = 0
        non_left_zero_pos = 0
        detect_left_zeros = True
        for d in lexeme_intent:
          if detect_left_zeros:
            if d == '0':
              non_left_zero_pos += 1
            else:
              detect_left_zeros = False
          if d == '.':
            dot_count += 1
        lexeme_intent = lexeme_intent[non_left_zero_pos:]
        if len(lexeme_intent) == 0:
          lexeme_intent = "0"
        if dot_count < 2:
          new_token_t = Gtoken.token_types[Gtoken.Number]
          if dot_count == 1:
            if lexeme_intent[0] == '.':
              lexeme_intent = "0" + lexeme_intent
            elif lexeme_intent[-1] == '.':
              lexeme_intent += "0"
        if inflection_char == '-':
          lexeme_intent = inflection_char + lexeme_intent
        if lexeme_intent[-1] == '.':
          lexeme_intent += "0"
    else:
      if inflection_char in Gtoken.special_single_symbols:
        lexeme_intent += inflection_char
        new_token_t = Gtoken.special_single_symbols[inflection_char]
      elif inflection_char == '=':
        if char_source.peek() == '=':
          char_source.get()
          lexeme_intent = "=="
          new_token_t = Gtoken.token_types[Gtoken.Comparator_op]
        else:
          lexeme_intent = "="
          new_token_t = Gtoken.token_types[Gtoken.Assign_op]
      elif inflection_char == '!':
        if char_source.peek() == '=':
          char_source.get()
          lexeme_intent = "!="
          new_token_t = Gtoken.token_types[Gtoken.Comparator_op]
        else:
          lexeme_intent = "!"
          new_token_t = Gtoken.token_types[Gtoken.Boolean_op]
      elif inflection_char == '<':
        if char_source.peek() == '=':
          char_source.get()
          lexeme_intent = "<="
        else:
          lexeme_intent = "<"
        new_token_t = Gtoken.token_types[Gtoken.Comparator_op]
      elif inflection_char == '>':
        if char_source.peek() == '=':
          char_source.get()
          lexeme_intent = ">="
        else:
          lexeme_intent = ">"
        new_token_t = Gtoken.token_types[Gtoken.Comparator_op]
      elif inflection_char == '&' and char_source.peek() == '&':
        char_source.get()
        lexeme_intent = "&&"
        new_token_t = Gtoken.token_types[Gtoken.Boolean_op]
      elif inflection_char == '|' and char_source.peek() == '|':
        char_source.get()
        lexeme_intent = "||"
        new_token_t = Gtoken.token_types[Gtoken.Boolean_op]
      elif inflection_char == '\'':
        ignore_next_char = False
        closed_string = False
        next_str_char = 0
        while not char_source.eof():
          next_str_char = char_source.get()
          if ignore_next_char == True:
            ignore_next_char = False
          else:
            if next_str_char == '\'':
              closed_string = True
              break
            if next_str_char == '\\':
              ignore_next_char = True
              continue
          lexeme_intent += next_str_char
        if closed_string:
          new_token_t = Gtoken.token_types[Gtoken.String]
    gen_token = Gtoken.Token(new_token_t, lexeme_intent, new_token_t is None)
    tokens.append(gen_token)
  return tokens