package __smbase;

public class PosterThread implements Runnable {

    private int delay;
    private Event event;
    private EventQueue eventQueue;
    
    public PosterThread(Event e, EventQueue q, int d){
	Thread t;
	
	event = e;
	eventQueue = q;
	delay = d;

	t = new Thread(this);
	t.setPriority(Thread.MAX_PRIORITY);
	t.start();
    }
    
    public void run(){
	try{
	    Thread.currentThread().sleep(delay);
	} catch(InterruptedException e) { 
	    e.printStackTrace();
	}
	
	eventQueue.put(event);
    }
}
