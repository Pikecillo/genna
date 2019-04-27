
#ifndef BLOCK_H
#define BLOCK_H

#include "all_definitions.h"

#include "Block.h"

class Block {
  public:
    static const int L = 4;
    static const int O = 7;
    static const int T = 1;
    static const int S = 2;
    static const int Z = 6;
    static const int J = 5;
    static const int VOID = 0;
    static const int I = 3;

  private:
    int kind;
    int coordinates [8];

  public:

    Block moveDown();

    int getKind();

    int * getCoordinates();

    Block moveRight();

    Block(int k);

    Block rotate();

    Block moveLeft();

    Block(const Block & b);
};

#endif
