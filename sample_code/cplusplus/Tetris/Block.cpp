
#include "Block.h"

Block Block::moveDown() {
    Block b(*this);
    int i = 0;

    int __action__ = 1;

    while(true) {
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
            b.coordinates[i + 1] += 1;
            i += 2;
            __action__ = 1;
            break;

            case 3:
            return b;
        }
    }
}

int Block::getKind() {
    return kind;
}

int * Block::getCoordinates() {
    return coordinates;
}

Block Block::moveRight() {
    Block b(*this);
    int i = 0;

    int __action__ = 0;

    while(true) {
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
            b.coordinates[i] += 1;
            i += 2;
            __action__ = 0;
            break;

            case 3:
            return b;
        }
    }
}

Block::Block(int k) {
    int *coord, i = 0;
    static int Oc[] = {5, 1, 4, 1, 4, 2, 5, 2};
    static int Tc[] = {5, 1, 6, 1, 4, 1, 5, 2};
    static int Sc[] = {5, 1, 6, 1, 4, 2, 5, 2};
    static int Ic[] = {4, 2, 3, 2, 5, 2, 6, 2};
    static int Lc[] = {5, 1, 4, 1, 6, 1, 4, 2};
    static int Jc[] = {5, 1, 4, 1, 6, 1, 6, 2};
    static int Zc[] = {5, 1, 4, 1, 5, 2, 6, 2};
    static int *coords[] = {0, Tc, Sc, Ic, Lc, Jc, Zc, Oc};

    int __action__ = 2;

    while(true) {
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
            kind = k;
            coord = coords[k];
            __action__ = 0;
            break;

            case 3:
            coordinates[i] = *(coord + i);
            i++;
            __action__ = 0;
            break;

            case 4:
            return;
        }
    }
}

Block Block::rotate() {
    Block b(*this);
    int i = 2, xc = coordinates[0], yc = coordinates[1], s = xc + yc, d = xc - yc;

    int __action__ = 2;

    while(true) {
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
            if(b.kind != Block::O) {
                __action__ = 1;
            }
            else {
                __action__ = 4;
            }
            break;

            case 3:
            b.coordinates[i] = coordinates[i + 1] + d;
            b.coordinates[i + 1] = s - coordinates[i];
            i += 2;
            __action__ = 1;
            break;

            case 4:
            return b;
        }
    }
}

Block Block::moveLeft() {
    Block b(*this);
    int i = 0;

    int __action__ = 1;

    while(true) {
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
            return b;;
        }
    }
}

Block::Block(const Block & b) {
    int i = 0;

    int __action__ = 3;

    while(true) {
        switch(__action__) {
            case 0:
            if(i < 8) {
                __action__ = 2;
            }
            else {
                __action__ = 4;
            }
            break;

            case 2:
            coordinates[i] = b.coordinates[i];
            i++;
            __action__ = 0;
            break;

            case 3:
            kind = b.kind;
            __action__ = 0;
            break;

            case 4:
            return;
        }
    }
}
