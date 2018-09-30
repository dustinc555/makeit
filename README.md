# makeit
A python script to generate a makefile for an existing C++ project


## Instructions
While in your project directory:
1) ```git clone https://github.com/dustinc555/makeit.git```
2) ```./makeit/makeit.py```
3) ```make```

## possible flags

* --dir "the desired working directory if blank uses current working directory"
* --flags "any additional compilation flags for the compiler"

## Note:
  * Currently only works for .cpp files all in the same directory
  
## TODO:
  * Make it so that it goes down into sub directories looking for either c or c++ files.
  * Make it so that the Makefile handles paths for you: #include "file.h" insted of #include "path/file.h"
