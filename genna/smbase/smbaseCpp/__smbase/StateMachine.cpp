#include "StateMachine.h"
#include "PosterThread.h"
#include "TopState.h"

namespace __smbase{

  StateMachine::StateMachine(void *c){
    
    terminated = false;

    context = c;
    top = new TopState(this);

    start();
  }

  StateMachine::~StateMachine(){
    delete top;
  }

  void StateMachine::postEvent(Event *e){

    if(QThread::currentThread() != this){
      othersQueue.put(e);
      return;
    }

    PosterThread *p = new PosterThread(e, &othersQueue, 0);

    terminatedMutex.lock();
    if(!terminated){
      cleanThreads(posterThreads);
      posterThreads.push_back(p);
    } else {
      p->wait();
      delete p;
    }
    terminatedMutex.unlock();
  }

  void StateMachine::setInnermostActive(State *s){
    innermostActive = s;
  }

  State *StateMachine::getInnermostActive(){
    return innermostActive;
  }

  void StateMachine::run(){
    State *source, *target, *lca;
    Event *event;
    EventHandle *handle;

    init();

    completionQueue.push(new Event(COMPLETION));

    while(true){
      
      if(completionQueue.empty())
	event = othersQueue.get();
      else{
	event = completionQueue.front();
	completionQueue.pop();
      }

      if(event->getName() == DIE){
	terminated = true;
	delete event;
	break;
      }

      source = innermostActive;

      do{
	handle = source->handleEvent(event);

	if(handle != 0){
	  target = handle->getTarget();
	  break;
	}

	source = source->getDirectAncestor();
      }while(source != top);

      if(source == top || (event->getName() == COMPLETION &&
	 source != innermostActive) || (event->getName() == COMPLETED &&
	 source != innermostActive->getDirectAncestor())){
	delete event;
        delete handle;
        continue;
      }

      lca = leastCommonAncestor(innermostActive, target);
      makeExit(innermostActive, lca);
      executeEffect(handle->getTransitionSequence());
      innermostActive = target;
      makeEntry(lca, innermostActive);
      innermostActive->doActivity();

      delete event;
      delete handle;
    }

    terminatedMutex.lock();
    waitThreads(posterThreads);
    terminatedMutex.unlock();

    waitThreads(timedThreads);
  }

  void StateMachine::postCompletionEvent(Event *e){
    completionQueue.push(e);
  }

  void StateMachine::postTimeEvent(Event *e, int when){
    cleanThreads(timedThreads);
    timedThreads.push_back(new PosterThread(e, &othersQueue, when));
  }

  void StateMachine::makeExit(State *from, State *to){
    State *actual = from;

    while(actual != to){
      actual->exit();
      actual = actual->getDirectAncestor();
    }
  }

  void StateMachine::makeEntry(State *from, State *to){
    
    if(from == to)
      return;

    makeEntry(from, to->getDirectAncestor());
    to->entry();
  }

  State *StateMachine::leastCommonAncestor(State *a, State *b){
    std::vector<State *> aList, bList, *xList;
    State *x;

    for(int i = 0 ; i < 2 ; i++){
      x = i == 0 ? a : b;
      xList = i == 0 ? &aList : &bList;

      while(x != top){
	xList->push_back(x);
	x = x->getDirectAncestor();
      }
    }

    while((x = aList.back()) == bList.back()){
      aList.pop_back();
      bList.pop_back();
      
      if(aList.empty() || bList.empty())
	break;
    }

    return x->getDirectAncestor();
  }

  void StateMachine::executeEffect(std::vector<Transition *> effectSequence){
    Transition *t;

    for(unsigned int i = 0 ; i < effectSequence.size() ; i++){
      t = effectSequence[i];

      if(t->hasEffect())
	t->executeEffect();
    }
  }

  void StateMachine::cleanThreads(std::vector<PosterThread *> &pt){
    std::vector<PosterThread *>::iterator i = pt.begin();

    while(i != pt.end()){
      if((*i)->isFinished()){
	delete *i;
	*i = 0;
	i = pt.erase(i);
      }
      else{
	i++;
      }
    }

  }

  void StateMachine::waitThreads(std::vector<PosterThread *> pt){

    std::vector<PosterThread *>::iterator i = pt.begin();
    
    while(i != pt.end()){
      if((*i)->isRunning()){
	(*i)->terminate();
	(*i)->wait(10);
      }
      (*i)->wait();
      delete *i;

      i++;
    }
  }
}
