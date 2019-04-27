#include "EventHandle.h"

namespace __smbase{

  EventHandle::EventHandle(std::vector<Transition *> ts, State *t){
    transitionSequence = ts;
    target = t;
  }

  std::vector<Transition *> EventHandle::getTransitionSequence(){
    return transitionSequence;
  }

  State *EventHandle::getTarget(){
    return target;
  }
}
