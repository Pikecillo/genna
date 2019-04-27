package __smbase;

import java.util.Queue;
import java.util.LinkedList;

public abstract class StateMachine implements Runnable{

    protected Object context;
    protected State innermostActive;
    protected State top;
    private EventQueue othersQueue;
    private Queue<Event> completionQueue;
    
    public final static int COMPLETION = -1;
    public final static int COMPLETED = -2;

    protected abstract void init();

    protected StateMachine(Object c){

	Thread t;

	context = c;
	othersQueue = new EventQueue();
        completionQueue = new LinkedList<Event>();
	top = new TopState(this);

	init();

	t = new Thread(this);

	t.start();
    }

    public void postEvent(Event e){
	new PosterThread(e, othersQueue, 0);
    }

    public void setInnermostActive(State s){
	innermostActive = s;
    }

    public State getInnermostActive(){
	return innermostActive;
    }

    public void run(){
	State source, target, lca;
	Event event;
	EventHandle handle;

	completionQueue.offer(new Event(COMPLETION));

	while(true){

            if(completionQueue.isEmpty())
	        event = othersQueue.get();
	    else
                event = completionQueue.poll();

            source = innermostActive;
	    target = null;

	    do{
		handle = source.handleEvent(event);
		
		if(handle != null){
		    target = handle.getTarget();
		    break;
		}
		
		source = source.getDirectAncestor();
	    }while(source != top);
	    
	    if(target == null)
		continue;

	    if(event.getName() == COMPLETED &&
	       source != innermostActive.getDirectAncestor())
		continue;

	    if(event.getName() == COMPLETION &&
	       source != innermostActive)
		continue;

	    lca = leastCommonAncestor(innermostActive, target);
	    makeExit(innermostActive, lca);
	    executeEffect(handle.getTransitionSequence());
	    innermostActive = target;
	    makeEntry(lca, innermostActive);
	    innermostActive.doActivity();

	}
    }

    protected void postCompletionEvent(Event e){
        completionQueue.offer(e);
    }

    protected void postTimeEvent(Event e, int when){
        new PosterThread(e, othersQueue, when);
    }

    private void makeExit(State from, State to){
	
	State actual = from;

	while(actual != to){
	    actual.exit();
	    actual = actual.getDirectAncestor();
	}
    }

    private void makeEntry(State from, State to){
	
	if(from == to)
	    return;

	makeEntry(from, to.getDirectAncestor());
	to.entry();
    }

    private State leastCommonAncestor(State a, State b){
	
	LinkedList<State> aList, bList, xList;
	State x;

	aList = new LinkedList<State>();
	bList = new LinkedList<State>();

	for(int i = 0 ; i < 2 ; i++){
	    x = i == 0 ? a : b;
	    xList = i == 0 ? aList : bList;

	    while(x != top){
		xList.offer(x);
		x = x.getDirectAncestor();
	    }
	}

	x = aList.getLast();

	while(aList.removeLast() == bList.removeLast()){
	    if(aList.isEmpty() || bList.isEmpty())
		break;

	    x = aList.getLast();
	}

	return x.getDirectAncestor();
    }

    private void executeEffect(LinkedList<Transition> effectSequence){
	
	Transition t;
	
	for(int i = 0 ; i < effectSequence.size() ; i++){
	    t = effectSequence.get(i);
	    
	    if(t.hasEffect())
		t.executeEffect();
	}
    }

    private class TopState extends State {
	
	public TopState(StateMachine sm){
	    super(sm);
	}

	public EventHandle handleEvent(Event e){
	    return new EventHandle(null, null);
	}

	public void entry(){};
	public void doActivity(){};
	public void exit(){};
    }
}
