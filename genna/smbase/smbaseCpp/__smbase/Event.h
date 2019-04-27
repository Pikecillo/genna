
#ifndef SMBASE_EVENT_H
#define SMBASE_EVENT_H

namespace __smbase {
  
  class Event {
    
  private:
    int name;
    
  public:
    Event(int);
    int getName();
  };
}

#endif
