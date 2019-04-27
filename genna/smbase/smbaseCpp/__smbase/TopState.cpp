#include "TopState.h"

namespace __smbase{
 
  TopState::TopState(StateMachine *sm) : State(sm) {};
  
  inline EventHandle *TopState::handleEvent(Event *){ 
    return 0;
  }

  inline void TopState::entry(){}
  inline void TopState::doActivity(){}
  inline void TopState::exit(){}

}
