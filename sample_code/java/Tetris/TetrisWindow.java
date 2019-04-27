
import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.lang.String;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

public class TetrisWindow extends JFrame implements ActionListener {
    private JButton startNewGameButton;
    private JButton exitButton;
    private JButton pauseButton;
    private PlayerWidget player;

    public Insets getInsets() {
        return new Insets(40, 20, 20, 20);
    }

    public void start() {
        player.getEngine().start();
    }

    public void pause() {
        player.getEngine().pause();
    }

    public TetrisWindow() {
        JPanel panel = new JPanel();

        player = new PlayerWidget();
        startNewGameButton = new JButton("NewGame");
        pauseButton = new JButton("Pause");
        exitButton = new JButton("ExitTetris");

        startNewGameButton.addActionListener(this);
        pauseButton.addActionListener(this);
        exitButton.addActionListener(this);

        startNewGameButton.setFocusable(false);
        pauseButton.setFocusable(false);
        exitButton.setFocusable(false);
        panel.setFocusable(false);

        setLayout(new BorderLayout());
        panel.setLayout(new GridLayout(1, 3));

        panel.add(startNewGameButton);
        panel.add(pauseButton);
        panel.add(exitButton);

        getContentPane().add(player, BorderLayout.NORTH);
        getContentPane().add(panel, BorderLayout.SOUTH);

        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                dispose();
                System.exit(0);
            }
        });
        addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                switch(e.getKeyCode()) {
                    case KeyEvent.VK_UP:
                    player.getEngine().rotate();
                    break;
                    case KeyEvent.VK_DOWN:
                    player.getEngine().down();
                    break;
                    case KeyEvent.VK_RIGHT:
                    player.getEngine().right();
                    break;
                    case KeyEvent.VK_LEFT:
                    player.getEngine().left();
                    break;
                    case KeyEvent.VK_SPACE:
                    player.getEngine().drop();
                    break;
                }
            }
        });

        setTitle("Tetris");
        setSize(460, 540);
        setResizable(false);
    }

    public static void main(String [] args) {
        (new TetrisWindow()).setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {
        int __action__ = 1;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(e.getSource() == startNewGameButton) {
                    __action__ = 3;
                }
                else if(e.getSource() == pauseButton) {
                    __action__ = 2;
                }
                else if(e.getSource() == exitButton) {
                    __action__ = 4;
                }
                else {
                    __action__ = 6;
                }
                break;

                case 2:
                player.getEngine().pause();
                __action__ = 5;
                break;

                case 3:
                player.getEngine().start();
                __action__ = 5;
                break;

                case 4:
                System.exit(0);
                __action__ = 5;
                break;

                case 5:
                break __loop__;

                case 6:
                break __loop__;
            }
        }
    }
}
