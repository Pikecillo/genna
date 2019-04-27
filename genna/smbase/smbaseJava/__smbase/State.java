package __smbase;

import java.util.LinkedList;

public abstract class State {
    
    private State directAncestor;
    private LinkedList<Event> waitedTimeEvents;
    protected StateMachine stateMachine;
    
    public State(StateMachine sm){
	directAncestor = null;
	stateMachine = sm;
	waitedTimeEvents = new LinkedList<Event>();
    }
    
    public void setDirectAncestor(State d){
	directAncestor = d;
    }

    public State getDirectAncestor(){
	return directAncestor;
    }
    
    protected void addWaited(Event e){
	waitedTimeEvents.offer(e);
    }

    protected boolean isWaited(Event e){
	return waitedTimeEvents.contains(e);
    }

    protected void removeWaited(Event e){
	waitedTimeEvents.remove(e);
    }

    protected void clearWaited(){
	waitedTimeEvents.clear();
    }

    public abstract EventHandle handleEvent(Event e);
    public void entry() {};
    public void doActivity() {};
    public void exit() {};
}
