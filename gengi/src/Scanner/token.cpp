#include "Scanner/token.hpp"

gg::Token gg::generateToken(std::stringstream& charSource, bool& eof){
  bool found_token = false;
  std::string lexeme_intent = "";
  TokenType new_token_t;
  while(!found_token){
    lexeme_intent.push_back((char)charSource.peek());
    if(lexeme_intent == ">"){
      if(charSource.peek() == '>')
        continue;
      else{
        charSource.seekg(charSource.tellp());
        new_token_t = TokenType::OP_MTHAN;
        found_token = true;
      }
    }
    else if(lexeme_intent == ">>>"){
      lexeme_intent = "";
      bool confirm_commentary_end = false;
      while(!confirm_commentary_end){
        char new_intent = 0;
        while(!charSource.eof() && (new_intent = charSource.get()) != '<'){}
        charSource.seekp(charSource.tellg());
        if(new_intent == '<' && charSource.peek() == '<'){
          charSource.get();
          if(charSource.peek() == '<')
            confirm_commentary_end = true;
        }
      }
    }
    else if(lexeme_intent == "+"){
      charSource.seekg(charSource.tellp());
      if(charSource.peek() == '+')
        new_token_t = TokenType::OP_DSUM;
      else
        new_token_t = TokenType::OP_SUM;
      found_token = true;
    }
    else if(lexeme_intent == "-"){
      charSource.seekg(charSource.tellp());
      if(charSource.peek() == '-')
        new_token_t = TokenType::OP_DSUB;
      else
        new_token_t = TokenType::OP_SUB;
      found_token = true;
    }
    else if(lexeme_intent == "*"){
      charSource.seekg(charSource.tellp());
      new_token_t = TokenType::OP_MUL;
      found_token = true;
    }
    else if(lexeme_intent == "/"){
      charSource.seekg(charSource.tellp());
      new_token_t = TokenType::OP_DIV;
      found_token = true;
    }
  }
  if(charSource.eof())
    eof = true;
  return {new_token_t, lexeme_intent};
}

const char *TokenTypeTag[] = {
  "ID", "OP_SUM", "OP_DSUM", "OP_SUB", "OP_DSUB", "OP_MUL", "OP_DIV", "OP_MOD",
  "OP_LTHAN", "OP_MTHAN", "OP_LEQTHAN", "OP_MEQTHAN", "OP_EQUAL", "OP_EQVL",
  "OP_NEQVL", "OP_AND", "OP_OR", "OP_XOR", "OP_NOT", "BEGIN_PAREN", "END_PAREN",
  "COMMA", "SEMICOLON", "BEGIN_BRACES", "END_BRACES", "BEGIN_BRACKETS", "END_BRACKETS",
  "IF", "ELSE", "FUNCTION", "RETURN", "GNODE", "SET", "GET", "LINK", "SPAWN", "IMPORT",
  "AS", "SPECIAL_PREPR_BEGIN", "SPECIAL_PREPR_END", "STR_QUOT", "NUMBER", "NONE"
};

std::ostream& operator<<(std::ostream &out, const gg::Token &token) {
    out << '<' << "TAG: " << TokenTypeTag[token.type_] << ", " << token.lexeme_ << '>';
    return out;
}