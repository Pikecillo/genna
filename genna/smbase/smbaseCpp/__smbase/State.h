#ifndef SMBASE_STATE_H
#define SMBASE_STATE_H

#include <vector>
#include "Event.h"
#include "EventHandle.h"
#include "StateMachine.h"

namespace __smbase{
  
  class StateMachine;
  class EventHandle;
  
  class State {

  protected:
    StateMachine *stateMachine;
    State *directAncestor;

  private:
    std::vector<Event *> waitedTimeEvents;

  public:
    State(StateMachine *);
    virtual ~State();
    void setDirectAncestor(State *);
    State *getDirectAncestor();
    virtual EventHandle *handleEvent(Event *) = 0;
    virtual void entry();
    virtual void doActivity();
    virtual void exit();

  protected:
    void addWaited(Event *);
    bool isWaited(Event *);
    void removeWaited(Event *);
    void clearWaited();
  };
}

#endif
