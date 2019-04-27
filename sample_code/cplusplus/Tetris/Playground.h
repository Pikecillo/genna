
#ifndef PLAYGROUND_H
#define PLAYGROUND_H

#include <cstdlib>
#include <ctime>

#include "all_definitions.h"

#include "Block.h"

class Playground {
  private:
    int ** space;
    Block * actual;
    Block * next;

  public:

    ~Playground();

    void renewBlocks();

    int clearLines();

    Block * getNext();

    Playground();

    int ** getSpace();

    Block * getActual();

    void setActual(Block * b);

    void settle();
};

#endif
