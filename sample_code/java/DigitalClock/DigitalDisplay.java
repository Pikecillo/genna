
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Toolkit;
import javax.swing.JPanel;

public class DigitalDisplay extends JPanel {
    public final static int H = 0;
    public final static int S = 2;
    public final static int NONE = -1;
    public final static int M = 1;

    private int which;
    private int [] time;

    public void paint(Graphics g) {
        int i = 0, x = 10;

        int __action__ = 8;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(i < 3) {
                    __action__ = 2;
                }
                else {
                    __action__ = 9;
                }
                break;

                case 2:
                if(which == i) {
                    __action__ = 4;
                }
                else {
                    __action__ = 6;
                }
                break;

                case 3:
                if(i < 2) {
                    __action__ = 7;
                }
                else {
                    __action__ = 5;
                }
                break;

                case 4:
                g.setColor(Color.red);
                __action__ = 6;
                break;

                case 5:
                i++;
                x += 70;
                __action__ = 1;
                break;

                case 6:
                g.drawString(String.valueOf(time[i] / 10), x, 35);
                g.drawString(String.valueOf(time[i] % 10), x + 20, 35);
                __action__ = 3;
                break;

                case 7:
                g.setColor(Color.black);
                g.drawString(":", x + 50, 35);
                __action__ = 5;
                break;

                case 8:
                g.setColor(Color.white);
                g.fillRect(0, 0, 400, 50);
                g.setColor(Color.black);
                g.setFont(new Font(g.getFont().getName(), Font.BOLD, 30));
                __action__ = 1;
                break;

                case 9:
                break __loop__;
            }
        }
    }

    public DigitalDisplay(int h, int m, int s) {
        setPreferredSize(new Dimension(200, 50));

        time = new int[3];
        time[0] = h;
        time[1] = m;
        time[2] = s;
    }

    public void display(int h, int m, int s, int high) {
        time = new int[] {h, m, s};
        which = high;
        repaint();
    }
}
