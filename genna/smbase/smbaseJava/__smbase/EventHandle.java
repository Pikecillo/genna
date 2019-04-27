package __smbase;

import java.util.LinkedList;

public class EventHandle {

    private boolean isEnabled;
    private LinkedList<Transition> transitionSequence;
    private State target;

    public EventHandle(LinkedList<Transition> ts, State t){
	transitionSequence = ts;
	target = t;
    }

    public LinkedList<Transition> getTransitionSequence(){
	return transitionSequence;
    }

    public State getTarget(){
	return target;
    }
}
