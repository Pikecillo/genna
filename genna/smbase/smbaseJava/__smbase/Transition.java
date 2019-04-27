package __smbase;

public class Transition{

    private boolean gotEffect;

    public Transition(boolean ge){
	gotEffect = ge;
    }

    public boolean hasEffect(){
	return gotEffect;
    }

    public void executeEffect() {};
}
