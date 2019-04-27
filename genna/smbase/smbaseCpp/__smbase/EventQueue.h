#ifndef SMBASE_EVENTQUEUE_H
#define SMBASE_EVENTQUEUE_H

#include <queue>
#include <QMutex>
#include <QWaitCondition>
#include "Event.h"

namespace __smbase{

  class EventQueue{
  private:
    std::queue<Event *> myQueue;
    const unsigned int MAX_EVENTS;
    QMutex *mutex;
    QWaitCondition *full;
    QWaitCondition *empty;

  public:
    EventQueue();
    ~EventQueue();
    void put(Event *);
    Event* get();
  };
}

#endif
