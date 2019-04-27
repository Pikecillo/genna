
#include "Playground.h"

Playground::~Playground() {
    int i;

    int __action__ = 2;

    while(true) {
        switch(__action__) {
            case 1:
            if(i < 21) {
                __action__ = 4;
            }
            else {
                __action__ = 3;
            }
            break;

            case 2:
            delete actual;
            delete next;
            i = 0;
            __action__ = 1;
            break;

            case 3:
            delete [] space;
            __action__ = 5;
            break;

            case 4:
            delete [] space[i];
            i++;
            __action__ = 1;
            break;

            case 5:
            return;
        }
    }
}

void Playground::renewBlocks() {
    delete actual;

    actual = next;
    next = new Block(rand() % 7 + 1);
}

int Playground::clearLines() {
    int count, i = 0, j, lines = 0;

    int __action__ = 3;

    while(true) {
        switch(__action__) {
            case 0:
            if(space[i][j] != Block::VOID) {
                __action__ = 7;
            }
            else {
                __action__ = 13;
            }
            break;

            case 1:
            if(j < 10) {
                __action__ = 0;
            }
            else {
                __action__ = 6;
            }
            break;

            case 3:
            if(i < 21) {
                __action__ = 9;
            }
            else {
                __action__ = 15;
            }
            break;

            case 4:
            if(j < 10) {
                __action__ = 10;
            }
            else {
                __action__ = 11;
            }
            break;

            case 5:
            if(j > 0) {
                __action__ = 8;
            }
            else {
                __action__ = 14;
            }
            break;

            case 6:
            if(count == 10) {
                __action__ = 12;
            }
            else {
                __action__ = 11;
            }
            break;

            case 7:
            count++;
            __action__ = 13;
            break;

            case 8:
            space[j] = space[j-1];
            j--;
            __action__ = 5;
            break;

            case 9:
            count = 0;
            j = 0;
            __action__ = 1;
            break;

            case 10:
            space[0][j] = Block::VOID;
            j++;
            __action__ = 4;
            break;

            case 11:
            i++;
            __action__ = 3;
            break;

            case 12:
            lines++;
            delete [] space[i];
            j = i;
            __action__ = 5;
            break;

            case 13:
            j++;
            __action__ = 1;
            break;

            case 14:
            space[0] = new int[10];
            __action__ = 4;
            break;

            case 15:
            return lines;
        }
    }
}

Block * Playground::getNext() {
    return next;
}

Playground::Playground() {
    int i, j;

    int __action__ = 7;

    while(true) {
        switch(__action__) {
            case 0:
            if(j < 10) {
                __action__ = 4;
            }
            else {
                __action__ = 5;
            }
            break;

            case 1:
            if(i < 21) {
                __action__ = 6;
            }
            else {
                __action__ = 3;
            }
            break;

            case 3:
            srand(time(0));
            actual = new Block(rand() % 7 + 1);
            next = new Block(rand() % 7 + 1);
            __action__ = 8;
            break;

            case 4:
            space[i][j] = Block::VOID;
            j++;
            __action__ = 0;
            break;

            case 5:
            i++;
            __action__ = 1;
            break;

            case 6:
            space[i] = new int[10];
            j = 0;
            __action__ = 0;
            break;

            case 7:
            space = new int*[21];
            i = 0;
            __action__ = 1;
            break;

            case 8:
            return;
        }
    }
}

int ** Playground::getSpace() {
    return space;
}

Block * Playground::getActual() {
    return actual;
}

void Playground::setActual(Block * b) {
    delete actual;

    actual = b;
}

void Playground::settle() {
    int *x = actual->getCoordinates(), i = 0;

    int __action__ = 1;

    while(true) {
        switch(__action__) {
            case 1:
            if(i < 8) {
                __action__ = 3;
            }
            else {
                __action__ = 2;
            }
            break;

            case 2:
            renewBlocks();
            __action__ = 4;
            break;

            case 3:
            space[x[i + 1]][x[i]] = actual->getKind();
            i += 2;
            __action__ = 1;
            break;

            case 4:
            return;
        }
    }
}
