#include "Scanner/token.hpp"
#include <map>
#include <iostream>

const std::map<char, gg::TokenType> special_single_symbols = {
  {'+', gg::TokenType::OP_SUM}, {'-', gg::TokenType::OP_SUB}, {'*', gg::TokenType::OP_MUL},
  {'/', gg::TokenType::OP_DIV}, {'^', gg::TokenType::OP_XOR}, {'(', gg::TokenType::BEGIN_PAREN},
  {')', gg::TokenType::END_PAREN}, {',', gg::TokenType::COMMA}, {';', gg::TokenType::SEMICOLON},
  {'{', gg::TokenType::BEGIN_BRACES}, {'}', gg::TokenType::END_BRACES}, {'[', gg::TokenType::BEGIN_BRACKETS},
  {']', gg::TokenType::END_BRACKETS}, {'.', gg::TokenType::OP_DOT}, {'%', gg::TokenType::OP_MOD},
  {':', gg::TokenType::OP_FROM}
};

const std::map<std::string, gg::TokenType> reserved_keywords = {
  {"if", gg::TokenType::IF}, {"else", gg::TokenType::ELSE}, {"function", gg::TokenType::FUNCTION},
  {"return", gg::TokenType::RETURN}, {"gnode", gg::TokenType::GNODE}, {"set", gg::TokenType::SET},
  {"get", gg::TokenType::GET}, {"link", gg::TokenType::LINK}, {"spawn", gg::TokenType::SPAWN},
  {"import", gg::TokenType::IMPORT}, {"as", gg::TokenType::AS}, {"for", gg::TokenType::FOR}, 
  {"while", gg::TokenType::WHILE}, {"#preprocess_begin", gg::TokenType::SPECIAL_PREPR_BEGIN},
  {"#preprocess_end", gg::TokenType::SPECIAL_PREPR_END}
};

gg::Token gg::generateToken(std::stringstream& charSource, bool& eof){
  std::string lexeme_intent = "";
  TokenType new_token_t = TokenType::NONE;
  char inflection_char = 0;

  while((inflection_char = (char)charSource.get()) == ' '){}
  if(isalpha(inflection_char) || inflection_char == '_' || inflection_char == '#'){//reserved or id
    lexeme_intent.push_back(inflection_char);
    char next_tk_char = (char)charSource.peek();
    while(!charSource.eof() && (isalnum(next_tk_char) || next_tk_char == '_')){
      lexeme_intent.push_back(next_tk_char);
      charSource.get();
      next_tk_char = (char)charSource.peek();
    }
    if(charSource.eof()){eof = true;}
    else{
      if(reserved_keywords.count(lexeme_intent)){
        new_token_t = reserved_keywords.find(lexeme_intent)->second;
      }
      else{
        bool good_id = true;
        for(char& c : lexeme_intent){
          if(c != '_' && !isalnum(c)){
            good_id = false;
            break;
          }
        }
        if(good_id){
          new_token_t = TokenType::ID;
        }
      }
    }
  }
  else if(isdigit(inflection_char) || (isdigit((char)charSource.peek()) && (inflection_char == '.' || inflection_char == '-'))){//integer, decimal
    char next_tk_char = (char)charSource.peek();
    if(inflection_char != '-')
      lexeme_intent.push_back(inflection_char);
    while(!charSource.eof() && (isdigit(next_tk_char) || next_tk_char == '.')){
      lexeme_intent.push_back(next_tk_char);
      charSource.get();
      next_tk_char = (char)charSource.peek();
    }
    if(charSource.eof()){eof = true;}
    else{
      std::size_t dot_count = 0, non_left_zero_pos = 0;
      bool detect_left_zeros = true;
      for(char& d : lexeme_intent){
        if(detect_left_zeros){
          if(d == '0')
            ++non_left_zero_pos;
          else
            detect_left_zeros = false;
        }
        if(d == '.'){
          ++dot_count;
        }
      }
      lexeme_intent = lexeme_intent.substr(non_left_zero_pos);
      if(lexeme_intent.length() == 0)
        lexeme_intent = "0";
      if(dot_count < 2){
        new_token_t = TokenType::NUMBER;
        if(dot_count == 1){
          if(lexeme_intent[0] == '.')
            lexeme_intent = "0" + lexeme_intent;
          else if(lexeme_intent.back() == '.')
            lexeme_intent += "0";
        }
      }
      if(inflection_char == '-')
        lexeme_intent.insert(lexeme_intent.begin(), inflection_char);
    }
  }
  else{//is another symbol
    if(special_single_symbols.count(inflection_char)){
      lexeme_intent.push_back(inflection_char);
      new_token_t = special_single_symbols.find(inflection_char)->second;
    }
    else if(inflection_char == '='){
      if(charSource.peek() == '='){
        charSource.get();
        lexeme_intent = "==";
        new_token_t = TokenType::OP_EQVL;
      }
      else{
        lexeme_intent = "=";
        new_token_t = TokenType::OP_EQUAL;
      }
    }
    else if(inflection_char == '!'){
      if(charSource.peek() == '='){
        charSource.get();
        lexeme_intent = "!=";
        new_token_t = TokenType::OP_NEQVL;
      }
      else{
        lexeme_intent = "!";
        new_token_t = TokenType::OP_NOT;
      }
    }
    else if(inflection_char == '<'){
      if(charSource.peek() == '='){
        charSource.get();
        lexeme_intent = "<=";
        new_token_t = TokenType::OP_LEQTHAN;
      }
      else{
        lexeme_intent = "<";
        new_token_t = TokenType::OP_LTHAN;
      }
    }
    else if(inflection_char == '>'){
      if(charSource.peek() == '='){
        charSource.get();
        lexeme_intent = ">=";
        new_token_t = TokenType::OP_MEQTHAN;
      }
      else{
        lexeme_intent = ">";
        new_token_t = TokenType::OP_MTHAN;
      }
    }
    else if(inflection_char == '&' && charSource.peek() == '&'){
      charSource.get();
      lexeme_intent = "&&";
      new_token_t = TokenType::OP_AND;
    }
    else if(inflection_char == '|' && charSource.peek() == '|'){
      charSource.get();
      lexeme_intent = "||";
      new_token_t = TokenType::OP_OR;
    }
    else if(inflection_char == '\''){
      bool ignore_next_char = false, closed_string = false;
      char next_str_char = 0;
      while(!charSource.eof()){
        next_str_char = (char)charSource.get();
        if(ignore_next_char == true)
          ignore_next_char = false;
        else{
          if(next_str_char == '\''){
            closed_string = true;
            break;
          }
          if(next_str_char == '\\'){
            ignore_next_char = true;
            continue;
          }
        }
        lexeme_intent.push_back(next_str_char);
      }
      if(closed_string)
        new_token_t = TokenType::STRING;
    }
    else if(inflection_char == -1)
      new_token_t = TokenType::EOF_;
  }
  if(charSource.eof())
    eof = true;
  return {new_token_t, lexeme_intent, ((new_token_t == TokenType::NONE)?true:false)};
}

const char *TokenTypeTag[] = {
  "ID", "OP_SUM", "OP_SUB", "OP_MUL", "OP_DIV", "OP_MOD", "OP_FROM",
  "OP_LTHAN", "OP_MTHAN", "OP_LEQTHAN", "OP_MEQTHAN", "OP_EQUAL", "OP_EQVL",
  "OP_NEQVL", "OP_AND", "OP_OR", "OP_XOR", "OP_NOT", "OP_DOT", "BEGIN_PAREN", "END_PAREN",
  "COMMA", "SEMICOLON", "BEGIN_BRACES", "END_BRACES", "BEGIN_BRACKETS", "END_BRACKETS",
  "IF", "ELSE", "FUNCTION", "RETURN", "GNODE", "SET", "GET", "LINK", "SPAWN", "IMPORT",
  "AS", "FOR", "WHILE", "SPECIAL_PREPR_BEGIN", "SPECIAL_PREPR_END", "STRING", "NUMBER",
  "NONE", "EOF"
};

std::ostream& operator<<(std::ostream &out, const gg::Token &token) {
    out << '<' << "TAG: " << TokenTypeTag[token.type_] << ", " << token.lexeme_ << '>';
    return out;
}