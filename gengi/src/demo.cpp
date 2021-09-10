#include <iostream>
#include "GenGi.hpp"

int main(int args, char *argv[]){
  if(args == 2){
    gg::scan(argv[1]);
    return 0;
  }
  std::cerr << "No files given to compile.\n";
  return 1;
}