#include "Scanner/doc_scanner.hpp"
#include <algorithm>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#define GG_EXTENSION "gg"

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

void gg::scan(const char* file){
  if(belongExtension(file, GG_EXTENSION)){
    std::ifstream file_content_stream(file);
    if(file_content_stream.is_open()){
      std::stringstream content;
      std::string readed_content;
      while(!file_content_stream.eof()){
        readed_content.push_back((char)file_content_stream.get());
      }
      file_content_stream.close();
      cleanCode(readed_content);
      content.str(readed_content);
      std::cout << content.str() << std::endl;
      bool eof = false;
      while(!eof){
        std::cout << generateToken(content, eof) << std::endl;
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