#ifndef SMBASE_POSTERTHREAD_H
#define SMBASE_POSTERTHREAD_H

#include <QThread>
#include "Event.h"
#include "EventQueue.h"

namespace __smbase{

  class PosterThread : public QThread {
    
  private:
    int delay;
    Event *event;
    EventQueue *eventQueue;

  public:
    PosterThread(Event *, EventQueue *, int);
   
  protected:
    void run();
  };
}

#endif
