#ifndef SMBASE_STATEMACHINE_H
#define SMBASE_STATEMACHINE_H

#include <vector>
#include <queue>
#include <QThread>
#include <QMutex>
#include "Event.h"
#include "EventQueue.h"
#include "State.h"
#include "Transition.h"
#include "PosterThread.h"

namespace __smbase{
  
  class State;
  class Transition;

  class StateMachine : public QThread {

  public:
    static const int COMPLETION = -1;
    static const int COMPLETED = -2;
    static const int DIE = -3;

  protected:
    void *context;
    State *innermostActive;
    State *top;

  private:
    bool terminated;
    QMutex terminatedMutex;
    EventQueue othersQueue;
    std::queue<Event *> completionQueue;
    std::vector<PosterThread *> posterThreads;
    std::vector<PosterThread *> timedThreads;

  public:    
    void setInnermostActive(State *);
    State *getInnermostActive();  
    void postEvent(Event *);
    
  protected:
    StateMachine(void *c);
    virtual ~StateMachine();
    void run();
    void postCompletionEvent(Event *);
    void postTimeEvent(Event *, int);
    virtual void init() = 0;

  private:
    void makeExit(State *, State*);
    void makeEntry(State *, State *);
    State *leastCommonAncestor(State *, State *);
    void executeEffect(std::vector<Transition *>);
    void cleanThreads(std::vector<PosterThread *> &);
    void waitThreads(std::vector<PosterThread *>);
  };
}

#endif
