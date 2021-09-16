#ifndef KMP_HPP_
#define KMP_HPP_

#include <iostream>
#include <vector>

namespace lex{

  std::vector<std::size_t> kmp(std::string source, std::string pattern, std::vector<int32_t> aux);

  std::vector<int32_t> prefix(std::string pattern);

}

#endif//KMP_HPP_