
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import javax.swing.JPanel;

public class PlaygroundWidget extends JPanel {
    private Playground myPlayground;

    public void paint(Graphics g) {
        Color colorTable [] = {Color.black, Color.magenta, Color.green, Color.cyan, Color.orange, Color.blue, Color.red, Color.yellow};
        Color color;
        int [] c = null;
        int [][] s = null;
        int i = 0, j = 0;

        int __action__ = 7;

        __loop__: while(true) {
            switch(__action__) {
                case 0:
                if(j < 10) {
                    __action__ = 5;
                }
                else {
                    __action__ = 9;
                }
                break;

                case 1:
                if(i < 21) {
                    __action__ = 0;
                }
                else {
                    __action__ = 4;
                }
                break;

                case 3:
                if(myPlayground == null) {
                    __action__ = 11;
                }
                else {
                    __action__ = 8;
                }
                break;

                case 4:
                if(j < 8) {
                    __action__ = 6;
                }
                else {
                    __action__ = 10;
                }
                break;

                case 5:
                g.setColor(colorTable[s[i][j]]);
                g.fillRect(j * 20 + 1, i * 20 + 1, 18, 18);
                j++;
                __action__ = 0;
                break;

                case 6:
                g.setColor(colorTable[myPlayground.getActual().getKind()]);
                g.fillRect(c[j] * 20 + 1, c[j + 1] * 20 + 1, 18, 18);
                j += 2;
                __action__ = 4;
                break;

                case 7:
                g.setColor(Color.black);
                g.fillRect(0, 0, 200, 420);
                g.setColor(Color.white);
                g.drawLine(0, 59, 200, 59);
                g.drawLine(0, 60, 200, 60);
                __action__ = 3;
                break;

                case 8:
                c = myPlayground.getActual().getCoordinates();
                s = myPlayground.getSpace();
                i = 0;
                j = 0;
                __action__ = 1;
                break;

                case 9:
                i++;
                j = 0;
                __action__ = 1;
                break;

                case 10:
                break __loop__;

                case 11:
                break __loop__;
            }
        }
    }

    public PlaygroundWidget() {
        int border;

        myPlayground = null;
        setPreferredSize(new Dimension(200, 420));
    }

    public void draw(Playground pg) {
        myPlayground = pg;
        repaint();
    }
}
