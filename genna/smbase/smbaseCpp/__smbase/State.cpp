#include <algorithm>
#include "State.h"

namespace __smbase{

  State::State(StateMachine *sm){
    directAncestor = 0;
    stateMachine = sm;
  }

  State::~State(){}

  void State::entry(){};

  void State::doActivity(){};

  void State::exit(){};

  void State::setDirectAncestor(State *d){
    directAncestor = d;
  }

  State *State::getDirectAncestor(){
    return directAncestor;
  }

  void State::addWaited(Event *e){
    waitedTimeEvents.push_back(e);
  }

  bool State::isWaited(Event *e){
    std::vector<Event *>::iterator i;

    i = std::find(waitedTimeEvents.begin(), waitedTimeEvents.end(), e);
    
    return i != waitedTimeEvents.end();
  }

  void State::removeWaited(Event *e){
    std::vector<Event *>::iterator i;

    i = std::find(waitedTimeEvents.begin(), waitedTimeEvents.end(), e);

    if(i != waitedTimeEvents.end())
      waitedTimeEvents.erase(i);
  }

  void State::clearWaited(){
    waitedTimeEvents.clear();
  }
}
