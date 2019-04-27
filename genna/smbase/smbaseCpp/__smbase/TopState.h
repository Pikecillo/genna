#ifndef SMBASE_TOPSTATE_H
#define SMBASE_TOPSTATE_H

#include "State.h"
#include "StateMachine.h"

namespace __smbase{
  
  class TopState : public State {
    
  public:
    TopState(StateMachine *sm);
    EventHandle *handleEvent(Event *);
    void entry();
    void doActivity();
    void exit();
  };
}

#endif
