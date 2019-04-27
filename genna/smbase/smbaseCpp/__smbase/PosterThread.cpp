#include "PosterThread.h"

namespace __smbase{
  
  PosterThread::PosterThread(Event *e, EventQueue *q, int d){
    
    event = e;
    eventQueue = q;
    delay = d;

    this->start();
  }

  void PosterThread::run(){
    msleep(delay);
    eventQueue->put(event);
  }
}
