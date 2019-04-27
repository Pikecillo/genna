
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.lang.String;
import javax.swing.JButton;
import javax.swing.JFrame;

public class Clock extends JFrame implements ActionListener {
    private int minutes;
    private int seconds;
    private int hours;
    private DigitalDisplay cDisplay;
    private JButton inc;
    private JButton mode;
    private JButton dec;

    public void inc() {
        __mySM.postEvent(new __smbase.Event(__Increment));
    }

    public Clock() {
        hours = 0;
        minutes = 0;
        seconds = 0;

        setBounds(100, 100, 250, 120);

        cDisplay = new DigitalDisplay(hours, minutes, seconds);
        mode = new JButton("Mode");
        inc = new JButton("Inc");
        dec = new JButton("Dec");

        getContentPane().setLayout(new FlowLayout());
        getContentPane().add(cDisplay);
        getContentPane().add(mode);
        getContentPane().add(inc);
        getContentPane().add(dec);

        mode.addActionListener(this);
        inc.addActionListener(this);
        dec.addActionListener(this);

        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                dispose();
                System.exit(0);
            }
        });

        setResizable(false);

        __mySM = new ClockStateMachine(this);
    }

    public void dec() {
        __mySM.postEvent(new __smbase.Event(__Decrement));
    }

    public void actionPerformed(ActionEvent event) {
        int __action__ = 1;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(event.getSource() == mode) {
                    __action__ = 4;
                }
                else if(event.getSource() == inc) {
                    __action__ = 3;
                }
                else {
                    __action__ = 2;
                }
                break;

                case 2:
                dec();
                __action__ = 5;
                break;

                case 3:
                inc();
                __action__ = 5;
                break;

                case 4:
                modeButton();
                __action__ = 5;
                break;

                case 5:
                break __loop__;
            }
        }
    }

    public static void main(String args[]) {
        (new Clock()).setVisible(true);
    }

    public void modeButton() {
        __mySM.postEvent(new __smbase.Event(__ModeButton));
    }

    private ClockStateMachine __mySM;

    private static final int __ModeButton = 0;
    private static final int __Increment = 1;
    private static final int __Decrement = 2;
    private static final int __AntiIdle = 3;
    private static final int __Tick = 4;

    private void __SetHoursEntry() {
        setTitle("Digital Clock - Set H");
    }

    private void __SetHoursDoActivity() {
        cDisplay.display(hours, minutes, seconds, DigitalDisplay.H);
    }

    private void __DisplayEntry() {
        setTitle("Digital Clock");
    }

    private void __DisplayDoActivity() {
        cDisplay.display(hours, minutes, seconds, DigitalDisplay.NONE);
    }

    private void __SetMinutesEntry() {
        setTitle("Digital Clock - Set M");
    }

    private void __SetMinutesDoActivity() {
        cDisplay.display(hours, minutes, seconds, DigitalDisplay.M);
    }

    private void __SetSecondsEntry() {
        setTitle("Digital Clock - Set S");
    }

    private void __SetSecondsDoActivity() {
        cDisplay.display(hours, minutes, seconds, DigitalDisplay.S);
    }

    private void __T_15Effect() {
        hours = (hours + 1) % 24;
    }

    private void __T_3Effect() {
        hours = (hours + 23) % 24;
    }

    private void __T_9Effect() {
        minutes = (minutes + 59) % 60;
    }

    private void __T_10Effect() {
        seconds = (seconds + 1) % 60;
    }

    private void __T_13Effect() {
        seconds = (seconds + 59) % 60;
    }

    private void __T_16Effect() {
        minutes = (minutes + 1) % 60;
    }

    private void __T_14Effect() {
        seconds = ++seconds % 60;
        minutes = seconds == 0 ? ++minutes % 60 : minutes;
        hours = (minutes == 0 && seconds == 0) ? ++hours % 24 : hours;
    }

    private class ClockStateMachine extends __smbase.StateMachine {
        private __smbase.State setHours;
        private __smbase.State display;
        private __smbase.State setMinutes;
        private __smbase.State setSeconds;
        private __smbase.State setting;
        private __smbase.State finalSettings;
        private __smbase.State settingInitial;
        private __smbase.State iTop;

        private __smbase.Transition t_0;
        private __smbase.Transition t_1;
        private __smbase.Transition t_15;
        private __smbase.Transition t_3;
        private __smbase.Transition t_5;
        private __smbase.Transition t_9;
        private __smbase.Transition t_10;
        private __smbase.Transition t_11;
        private __smbase.Transition t_13;
        private __smbase.Transition t_16;
        private __smbase.Transition t_7;
        private __smbase.Transition t_4;
        private __smbase.Transition t_12;
        private __smbase.Transition t_14;
        private __smbase.Transition t_2;
        private __smbase.Transition t_6;
        private __smbase.Transition t_8;

        public ClockStateMachine(Object c) {
            super(c);
        }

        protected void init() {
            setting = new Setting(this);
            setHours = new SetHours(this);
            display = new Display(this);
            setMinutes = new SetMinutes(this);
            setSeconds = new SetSeconds(this);
            finalSettings = new FinalSettings(this);
            settingInitial = new SettingInitial(this);
            iTop = new ITop(this);
            t_0 = new T_0(false);
            t_1 = new T_1(false);
            t_15 = new T_15(true);
            t_3 = new T_3(true);
            t_5 = new T_5(false);
            t_9 = new T_9(true);
            t_10 = new T_10(true);
            t_11 = new T_11(false);
            t_13 = new T_13(true);
            t_16 = new T_16(true);
            t_7 = new T_7(false);
            t_4 = new T_4(false);
            t_12 = new T_12(false);
            t_14 = new T_14(true);
            t_2 = new T_2(false);
            t_6 = new T_6(false);
            t_8 = new T_8(false);

            setting.setDirectAncestor(top);
            setHours.setDirectAncestor(setting);
            display.setDirectAncestor(top);
            setMinutes.setDirectAncestor(setting);
            setSeconds.setDirectAncestor(setting);
            finalSettings.setDirectAncestor(setting);
            settingInitial.setDirectAncestor(setting);
            iTop.setDirectAncestor(top);

            innermostActive = iTop;
        }

        private class SetHours extends __smbase.State { 

            public SetHours(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Clock.__Decrement:

                    transitionSequence.offer(t_3);
                    handle = new __smbase.EventHandle(transitionSequence, setHours);
                    break;

                    case Clock.__ModeButton:

                    transitionSequence.offer(t_0);
                    handle = new __smbase.EventHandle(transitionSequence, setMinutes);
                    break;

                    case Clock.__AntiIdle:
                    if(isWaited(e)) {
                        transitionSequence.offer(t_12);
                        handle = new __smbase.EventHandle(transitionSequence, finalSettings);
                        removeWaited(e);
                    }
                    break;

                    case Clock.__Increment:

                    transitionSequence.offer(t_15);
                    handle = new __smbase.EventHandle(transitionSequence, setHours);
                    break;
                }
                return handle;
            }

            public void entry() {
                __smbase.Event e;

                ((Clock)context).__SetHoursEntry();

                e = new __smbase.Event(Clock.__AntiIdle);
                addWaited(e);
                postTimeEvent(e, 10000);
            }

            public void doActivity() {
                ((Clock)context).__SetHoursDoActivity();
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }

            public void exit() {
                clearWaited();
            }
        }

        private class Display extends __smbase.State { 

            public Display(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Clock.__Tick:
                    if(isWaited(e)) {
                        transitionSequence.offer(t_14);
                        handle = new __smbase.EventHandle(transitionSequence, display);
                        removeWaited(e);
                    }
                    break;

                    case Clock.__ModeButton:

                    transitionSequence.offer(t_1);
                    handle = new __smbase.EventHandle(transitionSequence, setting);
                    break;
                }
                return handle;
            }

            public void entry() {
                __smbase.Event e;

                ((Clock)context).__DisplayEntry();

                e = new __smbase.Event(Clock.__Tick);
                addWaited(e);
                postTimeEvent(e, 1000);
            }

            public void doActivity() {
                ((Clock)context).__DisplayDoActivity();
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }

            public void exit() {
                clearWaited();
            }
        }

        private class SetMinutes extends __smbase.State { 

            public SetMinutes(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Clock.__Decrement:

                    transitionSequence.offer(t_9);
                    handle = new __smbase.EventHandle(transitionSequence, setMinutes);
                    break;

                    case Clock.__ModeButton:

                    transitionSequence.offer(t_5);
                    handle = new __smbase.EventHandle(transitionSequence, setSeconds);
                    break;

                    case Clock.__AntiIdle:
                    if(isWaited(e)) {
                        transitionSequence.offer(t_7);
                        handle = new __smbase.EventHandle(transitionSequence, finalSettings);
                        removeWaited(e);
                    }
                    break;

                    case Clock.__Increment:

                    transitionSequence.offer(t_16);
                    handle = new __smbase.EventHandle(transitionSequence, setMinutes);
                    break;
                }
                return handle;
            }

            public void entry() {
                __smbase.Event e;

                ((Clock)context).__SetMinutesEntry();

                e = new __smbase.Event(Clock.__AntiIdle);
                addWaited(e);
                postTimeEvent(e, 10000);
            }

            public void doActivity() {
                ((Clock)context).__SetMinutesDoActivity();
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }

            public void exit() {
                clearWaited();
            }
        }

        private class SetSeconds extends __smbase.State { 

            public SetSeconds(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case Clock.__Decrement:

                    transitionSequence.offer(t_13);
                    handle = new __smbase.EventHandle(transitionSequence, setSeconds);
                    break;

                    case Clock.__ModeButton:

                    transitionSequence.offer(t_11);
                    handle = new __smbase.EventHandle(transitionSequence, display);
                    break;

                    case Clock.__AntiIdle:
                    if(isWaited(e)) {
                        transitionSequence.offer(t_4);
                        handle = new __smbase.EventHandle(transitionSequence, finalSettings);
                        removeWaited(e);
                    }
                    break;

                    case Clock.__Increment:

                    transitionSequence.offer(t_10);
                    handle = new __smbase.EventHandle(transitionSequence, setSeconds);
                    break;
                }
                return handle;
            }

            public void entry() {
                __smbase.Event e;

                ((Clock)context).__SetSecondsEntry();

                e = new __smbase.Event(Clock.__AntiIdle);
                addWaited(e);
                postTimeEvent(e, 10000);
            }

            public void doActivity() {
                ((Clock)context).__SetSecondsDoActivity();
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETION));
            }

            public void exit() {
                clearWaited();
            }
        }

        private class Setting extends __smbase.State { 

            public Setting(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETED:

                    transitionSequence.offer(t_2);
                    handle = new __smbase.EventHandle(transitionSequence, display);
                    break;
                }
                return handle;
            }

            public void entry() {
                if(this == stateMachine.getInnermostActive()) {
                    stateMachine.setInnermostActive(settingInitial);
                }
            }
        }

        private class FinalSettings extends __smbase.State { 

            public FinalSettings(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;
                return handle;
            }

            public void entry() {
            }

            public void doActivity() {
                postCompletionEvent(new __smbase.Event(__smbase.StateMachine.COMPLETED));
            }
        }

        private class SettingInitial extends __smbase.State { 

            public SettingInitial(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_6);
                    handle = new __smbase.EventHandle(transitionSequence, setHours);
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

        private class ITop extends __smbase.State { 

            public ITop(__smbase.StateMachine sm) {
                super(sm);
            }

            public __smbase.EventHandle handleEvent(__smbase.Event e) {
                __smbase.EventHandle handle = null;

                java.util.LinkedList<__smbase.Transition> transitionSequence = new java.util.LinkedList<__smbase.Transition>();

                switch(e.getName()) {
                    case __smbase.StateMachine.COMPLETION:

                    transitionSequence.offer(t_8);
                    handle = new __smbase.EventHandle(transitionSequence, display);
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

        private class T_0 extends __smbase.Transition {
            public T_0(boolean b) {
                super(b);
            }
        }

        private class T_1 extends __smbase.Transition {
            public T_1(boolean b) {
                super(b);
            }
        }

        private class T_15 extends __smbase.Transition {
            public T_15(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Clock)context).__T_15Effect();
            }
        }

        private class T_3 extends __smbase.Transition {
            public T_3(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Clock)context).__T_3Effect();
            }
        }

        private class T_5 extends __smbase.Transition {
            public T_5(boolean b) {
                super(b);
            }
        }

        private class T_9 extends __smbase.Transition {
            public T_9(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Clock)context).__T_9Effect();
            }
        }

        private class T_10 extends __smbase.Transition {
            public T_10(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Clock)context).__T_10Effect();
            }
        }

        private class T_11 extends __smbase.Transition {
            public T_11(boolean b) {
                super(b);
            }
        }

        private class T_13 extends __smbase.Transition {
            public T_13(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Clock)context).__T_13Effect();
            }
        }

        private class T_16 extends __smbase.Transition {
            public T_16(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Clock)context).__T_16Effect();
            }
        }

        private class T_7 extends __smbase.Transition {
            public T_7(boolean b) {
                super(b);
            }
        }

        private class T_4 extends __smbase.Transition {
            public T_4(boolean b) {
                super(b);
            }
        }

        private class T_12 extends __smbase.Transition {
            public T_12(boolean b) {
                super(b);
            }
        }

        private class T_14 extends __smbase.Transition {
            public T_14(boolean b) {
                super(b);
            }

            public void executeEffect() {
                ((Clock)context).__T_14Effect();
            }
        }

        private class T_2 extends __smbase.Transition {
            public T_2(boolean b) {
                super(b);
            }
        }

        private class T_6 extends __smbase.Transition {
            public T_6(boolean b) {
                super(b);
            }
        }

        private class T_8 extends __smbase.Transition {
            public T_8(boolean b) {
                super(b);
            }
        }
    }
}
