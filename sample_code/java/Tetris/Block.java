
public class Block {
    public final static int L = 4;
    public final static int O = 7;
    public final static int T = 1;
    public final static int S = 2;
    public final static int Z = 6;
    public final static int J = 5;
    public final static int VOID = 0;
    public final static int I = 3;

    private int kind;
    private int [] coordinates;

    public Block moveDown() {
        Block b = new Block(this);
        int i = 0;

        int __action__ = 0;
        Block __returned__;

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
                b.coordinates[i + 1] += 1;
                i += 2;
                __action__ = 0;
                break;

                case 3:
                __returned__ = b;
                break __loop__;
            }
        }

        return __returned__;
    }

    public int getKind() {
        return kind;
    }

    public int [] getCoordinates() {
        return coordinates;
    }

    public Block moveRight() {
        Block b = new Block(this);
        int i = 0;

        int __action__ = 1;
        Block __returned__;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(i < 8) {
                    __action__ = 2;
                }
                else {
                    __action__ = 3;
                }
                break;

                case 2:
                b.coordinates[i] += 1;
                i += 2;
                __action__ = 1;
                break;

                case 3:
                __returned__ = b;
                break __loop__;
            }
        }

        return __returned__;
    }

    public Block(int k) {
        int [] coord;
        int [] Ocoord = {5, 1, 4, 1, 4, 2, 5, 2};
        int [] Tcoord = {5, 1, 6, 1, 4, 1, 5, 2};
        int [] Scoord = {5, 1, 6, 1, 4, 2, 5, 2};
        int [] Icoord = {4, 2, 3, 2, 5, 2, 6, 2};
        int [] Lcoord = {5, 1, 4, 1, 6, 1, 4, 2};
        int [] Jcoord = {5, 1, 4, 1, 6, 1, 6, 2};
        int [] Zcoord = {5, 1, 4, 1, 5, 2, 6, 2};

        kind = k;

        switch(k) {
            case O: coord = Ocoord; break;
            case T: coord = Tcoord; break;
            case S: coord = Scoord; break;
            case I: coord = Icoord; break;
            case L: coord = Lcoord; break;
            case J: coord = Jcoord; break;
            default: coord = Zcoord; break;
        }

        coordinates = new int[8];
        for(int i = 0; i < 8; i++)
        coordinates[i] = coord[i];
    }

    public Block rotate() {
        Block b = new Block(this);
        int i = 0, xc = coordinates[0], yc = coordinates[1], s = xc + yc, d = xc - yc;

        int __action__ = 2;
        Block __returned__;

        __loop__: while(true) {
            switch(__action__) {
                case 0:
                if(i < 8) {
                    __action__ = 3;
                }
                else {
                    __action__ = 4;
                }
                break;

                case 2:
                if(b.kind == Block.O) {
                    __action__ = 4;
                }
                else {
                    __action__ = 0;
                }
                break;

                case 3:
                b.coordinates[i] = coordinates[i + 1] + d;
                b.coordinates[i + 1] = s - coordinates[i];
                i += 2;
                __action__ = 0;
                break;

                case 4:
                __returned__ = b;
                break __loop__;
            }
        }

        return __returned__;
    }

    public Block moveLeft() {
        Block b = new Block(this);
        int i = 0;

        int __action__ = 1;
        Block __returned__;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(i < 8) {
                    __action__ = 2;
                }
                else {
                    __action__ = 3;
                }
                break;

                case 2:
                b.coordinates[i] -= 1;
                i += 2;
                __action__ = 1;
                break;

                case 3:
                __returned__ = b;
                break __loop__;
            }
        }

        return __returned__;
    }

    public Block(Block b) {
        int i = 0;

        int __action__ = 2;

        __loop__: while(true) {
            switch(__action__) {
                case 1:
                if(i < 8) {
                    __action__ = 3;
                }
                else {
                    __action__ = 4;
                }
                break;

                case 2:
                kind = b.kind;
                coordinates = new int[10];
                __action__ = 1;
                break;

                case 3:
                coordinates[i] = b.coordinates[i];
                i++;
                __action__ = 1;
                break;

                case 4:
                break __loop__;
            }
        }
    }
}
