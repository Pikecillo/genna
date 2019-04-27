
public class Engine {
    private int clearedLines;
    private final static int RIGHT = 1;
    private int level;
    private final static int LEFT = 2;
    private final static int ROTATE = 3;
    private int score;
    private final static int DOWN = 0;
    private int speed;
    private Playground playground;
    private PlayerWidget playerWidget;

    public void pause() {
        __mySM.postEvent(new __smbase.Event(__Pause));
    }

    public void start() {
        __mySM.postEvent(new __smbase.Event(__Start));
    }

    public void drop() {
        __mySM.postEvent(new __smbase.Event(__Drop));
    }

    public void rotate() {
        __mySM.postEvent(new __smbase.Event(__Rotate));
    }

    public void down() {
        __mySM.postEvent(new __smbase.Event(__GoDown));
    }

    public void left() {
        __mySM.postEvent(new __smbase.Event(__GoLeft));
    }

    public void right() {
        __mySM.postEvent(new __smbase.Event(__GoRight));
    }

    public Engine(PlayerWidget w) {
        playerWidget = w;
        playground = null;
        __mySM = new EngineStateMachine(this);
    }

    private boolean isGameOver() {
        int [] c = playground.getActual().getCoordinates();
        int i = 0;

        int __action__ = 1;
        boolean __returned__;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(i < 8) {
                    __action__ = 2;
                }
                else {
                    __action__ = 4;
                }
                break;

                case 2:
                if(c[i+1] < 3) {
                    __action__ = 5;
                }
                else {
                    __action__ = 3;
                }
                break;

                case 3:
                i += 2;
                __action__ = 1;
                break;

                case 4:
                __returned__ = false;
                break __loop__;

                case 5:
                __returned__ = true;
                break __loop__;
            }
        }

        return __returned__;
    }

    private void setNewGame() {
        playground = new Playground();
        speed = 1000;
        clearedLines = 0;
        score = 0;
        level = 0;
    }

    private void draw() {
        playerWidget.getPlaygroundWidget().draw(playground);
        playerWidget.getNextWidget().draw(playground.getNext());
        playerWidget.actualizeNumbers(clearedLines, score, level);
    }

    private void move(int which) {
        Block b = playground.getActual(), moved = null;

        int __action__ = 2;

        __loop__: while(true) {
            switch(__action__) {
                case 0:
                __action__ = 1;
                case 1:
                if(isValid(moved)) {
                    __action__ = 6;
                }
                else {
                    __action__ = 9;
                }
                break;

                case 2:
                if(which == DOWN) {
                    __action__ = 8;
                }
                else if(which == RIGHT) {
                    __action__ = 5;
                }
                else if(which == LEFT) {
                    __action__ = 4;
                }
                else {
                    __action__ = 7;
                }
                break;

                case 4:
                moved = new Block(b.moveLeft());
                __action__ = 0;
                break;

                case 5:
                moved = new Block(b.moveRight());
                __action__ = 0;
                break;

                case 6:
                playground.setActual(moved);
                __action__ = 9;
                break;

                case 7:
                moved = new Block(b.rotate());
                __action__ = 0;
                break;

                case 8:
                moved = new Block(b.moveDown());
                __action__ = 0;
                break;

                case 9:
                break __loop__;
            }
        }
    }

    private void setSpeed() {
        int i = 0;
        int spe[] = {1000, 900, 800, 700, 500, 300, 200, 100, 50, 25};
        int lin[] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};

        int __action__ = 2;

        __loop__: while(true) {
            switch(__action__) {
                case 0:
                if(clearedLines < lin[i]) {
                    __action__ = 3;
                }
                else {
                    __action__ = 4;
                }
                break;

                case 2:
                if(i < 10) {
                    __action__ = 0;
                }
                else {
                    __action__ = 5;
                }
                break;

                case 3:
                level = i + 1;
                speed = spe[i];
                __action__ = 5;
                break;

                case 4:
                i++;
                __action__ = 2;
                break;

                case 5:
                break __loop__;
            }
        }
    }

    private void renew() {
        int clearedNow;

        playground.settle();
        clearedNow = playground.clearLines();
        clearedLines += clearedNow;
        score += (10 + (clearedNow * clearedNow) * 100);
        setSpeed();
        playerWidget.actualizeNumbers(clearedLines, score, level);
    }

    private boolean isSettled() {
        int [] c = playground.getActual().getCoordinates();
        int i = 0;
        int [][] s = playground.getSpace();

        int __action__ = 1;
        boolean __returned__;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(i < 8) {
                    __action__ = 2;
                }
                else {
                    __action__ = 5;
                }
                break;

                case 2:
                if(c[i + 1] == 20 || s[c[i + 1] + 1][c[i]] != Block.VOID) {
                    __action__ = 4;
                }
                else {
                    __action__ = 3;
                }
                break;

                case 3:
                i += 2;
                __action__ = 1;
                break;

                case 4:
                __returned__ = true;
                break __loop__;

                case 5:
                __returned__ = false;
                break __loop__;
            }
        }

        return __returned__;
    }

    private boolean isValid(Block b) {
        int i = 0;
        int [] c = b.getCoordinates();
        int [][] s = playground.getSpace();

        int __action__ = 1;
        boolean __returned__;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(i < 8) {
                    __action__ = 2;
                }
                else {
                    __action__ = 4;
                }
                break;

                case 2:
                if(c[i] < 0 || c[i] > 9 || c[i + 1] < 0 || c[i + 1] > 20 || s[c[i + 1]][c[i]] != Block.VOID) {
                    __action__ = 5;
                }
                else {
                    __action__ = 3;
                }
                break;

                case 3:
                i += 2;
                __action__ = 1;
                break;

                case 4:
                __returned__ = true;
                break __loop__;

                case 5:
                __returned__ = false;
                break __loop__;
            }
        }

        return __returned__;
    }

    private EngineStateMachine __mySM;

    private static final int __Start = 0;
    private static final int __Pause = 1;
    private static final int __Drop = 2;
    private static final int __GoRight = 3;
    private static final int __Rotate = 4;
    private static final int __GoLeft = 5;
    private static final int __GoDown = 6;
    private static final int __Gravity = 7;

    private void __GoingRightEntry() {
        move(RIGHT);
    }

    private void __HardFallingEntry() {
        move(DOWN);
    }

    private void __InitializedEntry() {
        setNewGame();
    }

    private void __OverEntry() {
        draw();
    }

    private void __DrawingEntry() {
        draw();
    }

    private void __RotatingEntry() {
        move(ROTATE);
    }

    private void __SoftFallingEntry() {
        move(DOWN);
    }

    private void __GoingLeftEntry() {
        move(LEFT);
    }

    private void __InMotionEntry() {
        setSpeed();
    }

    private void __T_2Effect() {
        setNewGame();
    }

    private void __T_24Effect() {
        setNewGame();
    }

    private boolean __T_0Guard() {
        return(isGameOver());
    }

    private void __T_10Effect() {
        renew();
    }

    private boolean __T_11Guard() {
        return(isSettled());
    }

    private boolean __T_20Guard() {
        return(isSettled());
    }

    private class EngineStateMachine extends __smbase.StateMachine {
        private __smbase.State goingRight;
        private __smbase.State hardFalling;
        private __smbase.State initialized;
        private __smbase.State over;
        private __smbase.State drawing;
        private __smbase.State rotating;
        private __smbase.State paused;
        private __smbase.State softFalling;
        private __smbase.State goingLeft;
        private __smbase.State inMotion;
        private __smbase.State initialInMotion;
        private __smbase.State initialTop;

        private __smbase.Transition t_2;
        private __smbase.Transition t_7;
        private __smbase.Transition t_8;
        private __smbase.Transition t_9;
        private __smbase.Transition t_14;
        private __smbase.Transition t_15;
        private __smbase.Transition t_16;
        private __smbase.Transition t_18;
        private __smbase.Transition t_22;
        private __smbase.Transition t_24;
        private __smbase.Transition t_1;
        private __smbase.Transition t_0;
        private __smbase.Transition t_3;
        private __smbase.Transition t_4;
        private __smbase.Transition t_5;
        private __smbase.Transition t_6;
        private __smbase.Transition t_10;
        private __smbase.Transition t_11;
        private __smbase.Transition t_12;
        private __smbase.Transition t_13;
        private __smbase.Transition t_17;
        private __smbase.Transition t_19;
        private __smbase.Transition t_20;
        private __smbase.Transition t_21;
        private __smbase.Transition t_23;

        public EngineStateMachine(Object c) {
            super(c);
        }

        protected void init() {
            inMotion = new InMotion(this);
            goingRight = new GoingRight(this);
            hardFalling = new HardFalling(this);
            initialized = new Initialized(this);
            over = new Over(this);
            drawing = new Drawing(this);
            rotating = new Rotating(this);
            paused = new Paused(this);
            softFalling = new SoftFalling(this);
            goingLeft = new GoingLeft(this);
            initialInMotion = new InitialInMotion(this);
            initialTop = new InitialTop(this);
            t_2 = new T_2(true);
            t_7 = new T_7(false);
            t_8 = new T_8(false);
            t_9 = new T_9(false);
            t_14 = new T_14(false);
            t_15 = new T_15(false);
            t_16 = new T_16(false);
            t_18 = new T_18(false);
            t_22 = new T_22(false);
            t_24 = new T_24(true);
            t_1 = new T_1(false);
            t_0 = new T_0(false);
            t_3 = new T_3(false);
            t_4 = new T_4(false);
            t_5 = new T_5(false);
            t_6 = new T_6(false);
            t_10 = new T_10(true);
            t_11 = new T_11(false);
            t_12 = new T_12(false);
            t_13 = new T_13(false);
            t_17 = new T_17(false);
            t_19 = new T_19(false);
            t_20 = new T_20(false);
            t_21 = new T_21(false);
            t_23 = new T_23(false);

            inMotion.setDirectAncestor(top);
            goingRight.setDirectAncestor(inMotion);
            hardFalling.setDirectAncestor(top);
            initialized.setDirectAncestor(top);
            over.setDirectAncestor(top);
            drawing.setDirectAncestor(inMotion);
            rotating.setDirectAncestor(inMotion);
            paused.setDirectAncestor(top);
            softFalling.setDirectAncestor(top);
            goingLeft.setDirectAncestor(inMotion);
            initialInMotion.setDirectAncestor(inMotion);
            initialTop.setDirectAncestor(top);

            innermostActive = initialTop;
        }

        private class GoingRight extends __smbase.State { 

            public GoingRight(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_5);

                    transitionSequence.offer(t_17);
                    handle = new __smbase.EventHandle(transitionSequence, drawing);
                    break;
                }
                return handle;
            }

            public void entry() {
                ((Engine)context).__GoingRightEntry();
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class HardFalling extends __smbase.State { 

            public HardFalling(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_21);

                    if(((Engine)context).__T_11Guard()) {
                        transitionSequence.offer(t_11);

                        if(((Engine)context).__T_0Guard()) {
                            transitionSequence.offer(t_0);
                            handle = new __smbase.EventHandle(transitionSequence, over);
                        }
                        else {
                            transitionSequence.offer(t_10);
                            handle = new __smbase.EventHandle(transitionSequence, inMotion);
                        }
                    }
                    else {
                        transitionSequence.offer(t_13);
                        handle = new __smbase.EventHandle(transitionSequence, hardFalling);
                    }
                    break;
                }
                return handle;
            }

            public void entry() {
                ((Engine)context).__HardFallingEntry();
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class Initialized extends __smbase.State { 

            public Initialized(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Engine.__Start:

                    transitionSequence.offer(t_7);
                    handle = new __smbase.EventHandle(transitionSequence, inMotion);
                    break;
                }
                return handle;
            }

            public void entry() {
                ((Engine)context).__InitializedEntry();
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class Over extends __smbase.State { 

            public Over(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Engine.__Start:

                    transitionSequence.offer(t_2);
                    handle = new __smbase.EventHandle(transitionSequence, inMotion);
                    break;
                }
                return handle;
            }

            public void entry() {
                ((Engine)context).__OverEntry();
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class Drawing extends __smbase.State { 

            public Drawing(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Engine.__GoDown:

                    transitionSequence.offer(t_22);
                    handle = new __smbase.EventHandle(transitionSequence, softFalling);
                    break;

                    case Engine.__Drop:

                    transitionSequence.offer(t_14);
                    handle = new __smbase.EventHandle(transitionSequence, hardFalling);
                    break;

                    case Engine.__GoRight:

                    transitionSequence.offer(t_15);
                    handle = new __smbase.EventHandle(transitionSequence, goingRight);
                    break;

                    case Engine.__Rotate:

                    transitionSequence.offer(t_16);
                    handle = new __smbase.EventHandle(transitionSequence, rotating);
                    break;

                    case Engine.__GoLeft:

                    transitionSequence.offer(t_18);
                    handle = new __smbase.EventHandle(transitionSequence, goingLeft);
                    break;
                }
                return handle;
            }

            public void entry() {
                ((Engine)context).__DrawingEntry();
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class Rotating extends __smbase.State { 

            public Rotating(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_6);

                    transitionSequence.offer(t_17);
                    handle = new __smbase.EventHandle(transitionSequence, drawing);
                    break;
                }
                return handle;
            }

            public void entry() {
                ((Engine)context).__RotatingEntry();
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class Paused extends __smbase.State { 

            public Paused(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Engine.__Start:

                    transitionSequence.offer(t_24);
                    handle = new __smbase.EventHandle(transitionSequence, inMotion);
                    break;

                    case Engine.__Pause:

                    transitionSequence.offer(t_9);
                    handle = new __smbase.EventHandle(transitionSequence, inMotion);
                    break;
                }
                return handle;
            }

            public void entry() {
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class SoftFalling extends __smbase.State { 

            public SoftFalling(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_23);
                    handle = new __smbase.EventHandle(transitionSequence, inMotion);
                    break;
                }
                return handle;
            }

            public void entry() {
                ((Engine)context).__SoftFallingEntry();
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class GoingLeft extends __smbase.State { 

            public GoingLeft(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_4);

                    transitionSequence.offer(t_17);
                    handle = new __smbase.EventHandle(transitionSequence, drawing);
                    break;
                }
                return handle;
            }

            public void entry() {
                ((Engine)context).__GoingLeftEntry();
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class InMotion extends __smbase.State { 

            public InMotion(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Engine.__Pause:

                    transitionSequence.offer(t_8);
                    handle = new __smbase.EventHandle(transitionSequence, paused);
                    break;

                    case Engine.__Gravity:
                    if(isWaited(e)) {
                        transitionSequence.offer(t_1);

                        if(((Engine)context).__T_20Guard()) {
                            transitionSequence.offer(t_20);

                            if(((Engine)context).__T_0Guard()) {
                                transitionSequence.offer(t_0);
                                handle = new __smbase.EventHandle(transitionSequence, over);
                            }
                            else {
                                transitionSequence.offer(t_10);
                                handle = new __smbase.EventHandle(transitionSequence, inMotion);
                            }
                        }
                        else {
                            transitionSequence.offer(t_19);
                            handle = new __smbase.EventHandle(transitionSequence, softFalling);
                        }
                        removeWaited(e);
                    }
                    break;
                }
                return handle;
            }

            public void entry() {
                __smbase.Event e;

                ((Engine)context).__InMotionEntry();

                e = new __smbase.Event(Engine.__Gravity);
                addWaited(e);
                postTimeEvent(e, speed);

                if(this == stateMachine.getInnermostActive()) {
                    stateMachine.setInnermostActive(initialInMotion);
                }
            }

            public void exit() {
                clearWaited();
            }
        }

        private class InitialInMotion extends __smbase.State { 

            public InitialInMotion(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_12);
                    handle = new __smbase.EventHandle(transitionSequence, drawing);
                    break;
                }
                return handle;
            }

            public void entry() {
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class InitialTop extends __smbase.State { 

            public InitialTop(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_3);
                    handle = new __smbase.EventHandle(transitionSequence, initialized);
                    break;
                }
                return handle;
            }

            public void entry() {
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }
        }

        private class T_2 extends __smbase.Transition {
            public T_2(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Engine)context).__T_2Effect();
            }
        }

        private class T_7 extends __smbase.Transition {
            public T_7(boolean b) {
                super(b);
            }
        }

        private class T_8 extends __smbase.Transition {
            public T_8(boolean b) {
                super(b);
            }
        }

        private class T_9 extends __smbase.Transition {
            public T_9(boolean b) {
                super(b);
            }
        }

        private class T_14 extends __smbase.Transition {
            public T_14(boolean b) {
                super(b);
            }
        }

        private class T_15 extends __smbase.Transition {
            public T_15(boolean b) {
                super(b);
            }
        }

        private class T_16 extends __smbase.Transition {
            public T_16(boolean b) {
                super(b);
            }
        }

        private class T_18 extends __smbase.Transition {
            public T_18(boolean b) {
                super(b);
            }
        }

        private class T_22 extends __smbase.Transition {
            public T_22(boolean b) {
                super(b);
            }
        }

        private class T_24 extends __smbase.Transition {
            public T_24(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Engine)context).__T_24Effect();
            }
        }

        private class T_1 extends __smbase.Transition {
            public T_1(boolean b) {
                super(b);
            }
        }

        private class T_0 extends __smbase.Transition {
            public T_0(boolean b) {
                super(b);
            }
        }

        private class T_3 extends __smbase.Transition {
            public T_3(boolean b) {
                super(b);
            }
        }

        private class T_4 extends __smbase.Transition {
            public T_4(boolean b) {
                super(b);
            }
        }

        private class T_5 extends __smbase.Transition {
            public T_5(boolean b) {
                super(b);
            }
        }

        private class T_6 extends __smbase.Transition {
            public T_6(boolean b) {
                super(b);
            }
        }

        private class T_10 extends __smbase.Transition {
            public T_10(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Engine)context).__T_10Effect();
            }
        }

        private class T_11 extends __smbase.Transition {
            public T_11(boolean b) {
                super(b);
            }
        }

        private class T_12 extends __smbase.Transition {
            public T_12(boolean b) {
                super(b);
            }
        }

        private class T_13 extends __smbase.Transition {
            public T_13(boolean b) {
                super(b);
            }
        }

        private class T_17 extends __smbase.Transition {
            public T_17(boolean b) {
                super(b);
            }
        }

        private class T_19 extends __smbase.Transition {
            public T_19(boolean b) {
                super(b);
            }
        }

        private class T_20 extends __smbase.Transition {
            public T_20(boolean b) {
                super(b);
            }
        }

        private class T_21 extends __smbase.Transition {
            public T_21(boolean b) {
                super(b);
            }
        }

        private class T_23 extends __smbase.Transition {
            public T_23(boolean b) {
                super(b);
            }
        }
    }
}
