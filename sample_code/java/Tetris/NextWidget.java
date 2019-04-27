
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import javax.swing.JPanel;

public class NextWidget extends JPanel {
    private Block nextBlock;

    public void paint(Graphics g) {
        Color [] colorTable = {Color.black, Color.magenta, Color.green, Color.cyan, Color.orange, Color.blue, Color.red, Color.yellow}; 
        int x = 0, k = 0, i = 0;
        int [] c = null;

        int __action__ = 3;

        __loop__: while(true) {
            switch(__action__) {
                case 0:
                if(nextBlock == null) {
                    __action__ = 6;
                }
                else {
                    __action__ = 4;
                }
                break;

                case 2:
                if(i < 8) {
                    __action__ = 5;
                }
                else {
                    __action__ = 6;
                }
                break;

                case 3:
                g.setColor(Color.black);
                g.fillRect(0, 0, 120, 80);

                __action__ = 0;
                break;

                case 4:
                c = nextBlock.getCoordinates();
                k = nextBlock.getKind();
                x = k == Block.I || k == Block.O ? 1 : 0;
                i = 0;
                __action__ = 2;
                break;

                case 5:
                g.setColor(colorTable[nextBlock.getKind()]);
                g.fillRect((c[i] - 3 + x) * 20 + 1, c[i + 1] * 20 + 1, 18, 18);
                i += 2;
                __action__ = 2;
                break;

                case 6:
                break __loop__;
            }
        }
    }

    public void draw(Block b) {
        nextBlock = b;
        repaint();
    }

    public NextWidget() {
        int border;

        nextBlock = null;

        setPreferredSize(new Dimension(120, 80));
    }
}
