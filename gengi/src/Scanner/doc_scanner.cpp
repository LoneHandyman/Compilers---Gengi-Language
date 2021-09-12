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

void gg::scan(const char* file){
  if(belongExtension(file, GG_EXTENSION)){
    std::ifstream file_content_stream(file, std::ios::binary);
    if(file_content_stream.is_open()){
      std::stringstream content;
      while(!file_content_stream.eof()){
        content << (char)file_content_stream.get();
      }
      std::cout << content.str() << std::endl;
      file_content_stream.close();
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