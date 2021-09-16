#ifndef TOKEN_HPP_
#define TOKEN_HPP_

#include <sstream>
#include <string>

namespace gg{

  enum TokenType{
    ID, OP_SUM, OP_SUB, OP_MUL, OP_DIV, OP_MOD, OP_FROM,
    OP_LTHAN, OP_MTHAN, OP_LEQTHAN, OP_MEQTHAN, OP_EQUAL, OP_EQVL,
    OP_NEQVL, OP_AND, OP_OR, OP_XOR, OP_NOT, OP_DOT,
    BEGIN_PAREN, END_PAREN, COMMA, SEMICOLON, BEGIN_BRACES, END_BRACES,
    BEGIN_BRACKETS, END_BRACKETS,
    IF, ELSE, FUNCTION, RETURN, GNODE, SET, GET, LINK, SPAWN, IMPORT, AS,
    FOR, WHILE, 
    SPECIAL_PREPR_BEGIN, SPECIAL_PREPR_END,
    STRING,
    NUMBER, NONE, EOF_
  };

  struct Token{
    TokenType type_;
    std::string lexeme_;
    bool bad_token_;

    Token(){}
    Token(const TokenType& type, const std::string& lexeme, bool bad_token = false):
      type_(type), lexeme_(lexeme), bad_token_(bad_token) {}
  };

  Token generateToken(std::stringstream& charSource, bool& eof);
}

std::ostream& operator<<(std::ostream &out, const gg::Token &token);

#endif//TOKEN_HPP_