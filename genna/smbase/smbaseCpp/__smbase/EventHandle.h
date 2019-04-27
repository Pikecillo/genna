#ifndef SMBASE_EVENTHANDLE_H
#define SMBASE_EVENTHANDLE_H

#include <vector>
#include "State.h"
#include "Transition.h"

namespace __smbase{

  class State;
  class Transition;

  class EventHandle {
    
  private:
    std::vector<Transition *> transitionSequence;
    State *target;

  public:
    EventHandle(std::vector<Transition *>, State *);
    std::vector<Transition *> getTransitionSequence();
    State *getTarget();
  };
}

#endif
