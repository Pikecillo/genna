#ifndef SMBASE_TRANSITION_H
#define SMBASE_TRANSITION_H

#include "StateMachine.h"

namespace __smbase {
  
  class StateMachine;

  class Transition {
    
  protected:
    bool gotEffect;
    StateMachine *stateMachine;

  public:
    Transition(bool, StateMachine *);
    virtual ~Transition();
    bool hasEffect();
    virtual void executeEffect();
  };
}

#endif
