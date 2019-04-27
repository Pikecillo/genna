#include "EventQueue.h"
#include "StateMachine.h"

namespace __smbase{

  EventQueue::EventQueue() : MAX_EVENTS(20) {
    mutex = new QMutex();
    full = new QWaitCondition();
    empty = new QWaitCondition();
  }

  EventQueue::~EventQueue(){
    delete mutex;
    delete full;
    delete empty;

    while(!myQueue.empty()){
      delete myQueue.front();
      myQueue.pop();
    } 
  }

  void EventQueue::put(Event *event){
    
    mutex->lock();
    
    if(myQueue.size() == MAX_EVENTS)
      empty->wait(mutex);
    
    myQueue.push(event);
    full->wakeAll(); 
    
    mutex->unlock();
  }

  Event *EventQueue::get(){

    Event *event;

    mutex->lock();

    if(myQueue.empty())
      full->wait(mutex);

    event = myQueue.front();
    myQueue.pop();

    if(myQueue.size() == 0)
      empty->wakeAll();

    mutex->unlock();

    return event;
  }
}
