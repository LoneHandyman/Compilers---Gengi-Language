# [UCSP - Compilers]: GenGi, A Game Programming Language

## Instrucciones:
- Construir el proyecto y compilar con cmake y make.
- `cmake -B build -G "MinGW Makefiles" ` en caso de Windows, sino usar el generador que tenga en su cmake.
- `cd build` -> `make` -> `./gg <archivo.gg>`. El programa simplemente recibe el archivo de código, en este caso **".gg"** como extensión personalizada.
- Como salida se imprimirá los pasos que sigue el analizador lexico: La lectura simple del código, la eliminación de comentarios, la eliminación de tabuladores y saltos de línea y por último, la extracción de los tokens en orden.