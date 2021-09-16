#include "Scanner/doc_scanner.hpp"
#include "Scanner/kmp.hpp"
#include <algorithm>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#define LANG_GENGI_EXTENSION "gg"

bool belongExtension(const char* file, const char* ext){
  std::stringstream file_name;
  std::string file_str(file);
  file_name.str({file_str.rbegin(), file_str.rend()});
  std::string file_ext;
  std::getline(file_name, file_ext, '.');
  return !(strcmp(ext, file_ext.c_str()));
}

void cleanCode(std::string& source){
  char last_got_char = ' ';
  bool str_mode = false;
  std::string src_copy;
  for(std::size_t idx = 0; idx < source.length(); ++idx){
    if(source[idx] == 39)
      str_mode = !str_mode;
    if(!str_mode){
      if(source[idx] == '\t' || source[idx] == '\n' || source[idx] == ' '){
        source[idx] = ' ';
        if(last_got_char == ' ')
          continue;
      }
    }
    src_copy.push_back(source[idx]);
    last_got_char = source[idx];
  }
  source = src_copy;
}

std::string cleanComments(std::vector<std::string>& code_lines){
  std::string merged_content = "";
  std::vector<std::size_t> comm_pos_begin;
  std::vector<int32_t> prefix_table = lex::prefix(">>>");
  for(std::size_t idx = 0; idx < code_lines.size(); ++idx){
    comm_pos_begin = lex::kmp(code_lines[idx], ">>>", prefix_table);
    if(comm_pos_begin.size())
      code_lines[idx] = code_lines[idx].substr(0, comm_pos_begin[0]);
    code_lines[idx] += "\n";
    merged_content += code_lines[idx];
  }
  return merged_content;
}

void gg::scan(const char* file){
  if(belongExtension(file, LANG_GENGI_EXTENSION)){
    std::ifstream file_content_stream(file);
    if(file_content_stream.is_open()){
      std::stringstream content;
      std::vector<std::string> readed_content;
      std::string code_line;
      while(!file_content_stream.eof()){
        std::getline(file_content_stream, code_line, '\n');
        std::cout << code_line << std::endl;
        readed_content.push_back(code_line);
      }
      file_content_stream.close();
      std::string fixed_content = cleanComments(readed_content);
      std::cout << fixed_content << std::endl;
      cleanCode(fixed_content);
      content.str(fixed_content);
      std::cout << content.str() << std::endl;
      bool eof = false;
      while(!eof){
        Token new_token = generateToken(content, eof);
        std::cout << new_token << std::endl;
        if(new_token.bad_token_)
          std::cerr << "[WARNING] -->>> GG-compiler: LEXICAL ERROR\n";
      }
    }
    else{
      std::cerr << "The given file doesn\'t exist.\n";
      exit(1);
    }
  }
  else{
    std::cerr << "Can only compile GenGi files with \"gg\" extension.\n";
    exit(1);
  }
}