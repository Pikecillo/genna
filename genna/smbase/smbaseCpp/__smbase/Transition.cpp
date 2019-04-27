#include "Transition.h"

namespace __smbase{

  Transition::Transition(bool ge, StateMachine *sm){
    gotEffect = ge;
    stateMachine = sm;
  }

  Transition::~Transition(){}

  bool Transition::hasEffect(){
    return gotEffect;
  }

  void Transition::executeEffect(){}
}
