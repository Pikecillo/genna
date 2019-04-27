package __smbase;

import java.util.LinkedList;
import java.util.Queue;

//Cola de eventos y despachador FIFO
public class EventQueue{

    private Queue<Event> myQueue;
    private final int MAX_EVENTS = 20;

    public EventQueue(){	    
	myQueue = new LinkedList<Event>();
    }
    
    public synchronized void put(Event event){

	if(myQueue.size() == MAX_EVENTS)
	    try{
		wait();
	    } catch(InterruptedException e1) { 
		e1.printStackTrace();
	    }

	myQueue.offer(event);

	try {
	    notifyAll();
	} catch(IllegalMonitorStateException e2){
	    e2.printStackTrace();
	}
    }
    
    public synchronized Event get(){    
	
	Event e;

	if(myQueue.isEmpty())
	    try{
		wait();
	    } catch(InterruptedException e1) {
		e1.printStackTrace();
	    }

	e = myQueue.poll();
	
        if(myQueue.size() == 0)
	    try {
		notifyAll();
	    } catch(IllegalMonitorStateException e2){
		e2.printStackTrace();
	    }

	return e;
    }
}
