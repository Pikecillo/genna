#include "Event.h"

namespace __smbase {

  Event::Event(int n){
    name = n;
  }

  int Event::getName(){
    return name;
  }
}
