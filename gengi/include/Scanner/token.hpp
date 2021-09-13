#ifndef TOKEN_HPP_
#define TOKEN_HPP_

#include <sstream>
#include <string>

namespace gg{

  enum TokenType{
    ID, OP_SUM, OP_DSUM, OP_SUB, OP_DSUB, OP_MUL, OP_DIV, OP_MOD,
    OP_LTHAN, OP_MTHAN, OP_LEQTHAN, OP_MEQTHAN, OP_EQUAL, OP_EQVL,
    OP_NEQVL, OP_AND, OP_OR, OP_XOR, OP_NOT, 
    BEGIN_PAREN, END_PAREN, COMMA, SEMICOLON, BEGIN_BRACES, END_BRACES,
    BEGIN_BRACKETS, END_BRACKETS,
    IF, ELSE, FUNCTION, RETURN, GNODE, SET, GET, LINK, SPAWN, IMPORT, AS, 
    SPECIAL_PREPR_BEGIN, SPECIAL_PREPR_END,
    STR_QUOT,
    NUMBER, NONE
  };

  struct Token{
    TokenType type_;
    std::string lexeme_;

    Token(){}
    Token(const TokenType& type, const std::string& lexeme):type_(type), lexeme_(lexeme) {}
  };

  Token generateToken(std::stringstream& charSource, bool& eof);
}

std::ostream& operator<<(std::ostream &out, const gg::Token &token);

#endif//TOKEN_HPP_