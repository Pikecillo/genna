
import java.util.Random;

public class Playground {
    private int [][] space;
    private Random rand;
    private Block actual;
    private Block next;

    public void renewBlocks() {
        actual = next;
        next = new Block(rand.nextInt(7) + 1);
    }

    public int clearLines() {
        int count = 0, i = 0, j = 0, lines = 0;

        int __action__ = 5;
        int __returned__;

        __loop__: while(true) {
            switch(__action__) {
                case 0:
                if(count == 10) {
                    __action__ = 11;
                }
                else {
                    __action__ = 9;
                }
                break;

                case 1:
                if(space[i][j] != Block.VOID) {
                    __action__ = 12;
                }
                else {
                    __action__ = 13;
                }
                break;

                case 2:
                if(j < 10) {
                    __action__ = 1;
                }
                else {
                    __action__ = 0;
                }
                break;

                case 3:
                if(j > 0) {
                    __action__ = 10;
                }
                else {
                    __action__ = 14;
                }
                break;

                case 4:
                if(j < 10) {
                    __action__ = 8;
                }
                else {
                    __action__ = 9;
                }
                break;

                case 5:
                if(i < 21) {
                    __action__ = 7;
                }
                else {
                    __action__ = 15;
                }
                break;

                case 7:
                count = 0;
                j = 0;
                __action__ = 2;
                break;

                case 8:
                space[0][j] = Block.VOID;
                j++;
                __action__ = 4;
                break;

                case 9:
                i++;
                __action__ = 5;
                break;

                case 10:
                space[j] = space[j-1];
                j--;
                __action__ = 3;
                break;

                case 11:
                lines ++;
                j = i;
                __action__ = 3;
                break;

                case 12:
                count++;
                __action__ = 13;
                break;

                case 13:
                j++;
                __action__ = 2;
                break;

                case 14:
                space[0] = new int[10];
                j = 0;
                __action__ = 4;
                break;

                case 15:
                __returned__ = lines;
                break __loop__;
            }
        }

        return __returned__;
    }

    public Block getNext() {
        return next;
    }

    public Playground() {
        int i = 0, j = 0;

        int __action__ = 5;

        __loop__: while(true) {
            switch(__action__) {
                case 0:
                if(i < 21) {
                    __action__ = 2;
                }
                else {
                    __action__ = 6;
                }
                break;

                case 2:
                __action__ = 4;

                case 3:
                i++;
                j = 0;
                __action__ = 0;
                break;

                case 4:
                space[i][j] = Block.VOID;
                j++;
                __action__ = 2;
                break;

                case 5:
                space = new int[21][10];
                __action__ = 0;
                break;

                case 6:
                rand = new Random();
                actual = new Block(rand.nextInt(7) + 1);
                next = new Block(rand.nextInt(7) + 1);
                __action__ = 7;
                break;

                case 7:
                break __loop__;
            }
        }
    }

    public int [][] getSpace() {
        return space;
    }

    public Block getActual() {
        return actual;
    }

    public void setActual(Block b) {
        actual = b;
    }

    public void settle() {
        int i = 0;
        int [] x = actual.getCoordinates();

        int __action__ = 0;

        __loop__: while(true) {
            switch(__action__) {
                case 0:
                if(i < 8) {
                    __action__ = 2;
                }
                else {
                    __action__ = 3;
                }
                break;

                case 2:
                space[x[i + 1]][x[i]] = actual.getKind();
                i += 2;
                __action__ = 0;
                break;

                case 3:
                renewBlocks();
                __action__ = 4;
                break;

                case 4:
                break __loop__;
            }
        }
    }
}
