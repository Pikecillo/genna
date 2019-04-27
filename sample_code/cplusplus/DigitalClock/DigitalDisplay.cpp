
#include "DigitalDisplay.h"

DigitalDisplay::DigitalDisplay() {
    time[0] = 0;
    time[1] = 0;
    time[2] = 0;

    setFixedSize(230, 50);
}

void DigitalDisplay::show(int h, int m, int s, int high) {
    time[0] = h;
    time[1] = m;
    time[2] = s;
    which = high;
    update();
}

void DigitalDisplay::paintEvent(QPaintEvent * e) {
    int i = 0, x = 40;
    QString d;
    QPainter painter(this);
    QFont f;

    int __action__ = 8;

    while(true) {
        switch(__action__) {
            case 0:
            if(which == i) {
                __action__ = 4;
            }
            else {
                __action__ = 7;
            }
            break;

            case 1:
            if(i < 2) {
                __action__ = 6;
            }
            else {
                __action__ = 5;
            }
            break;

            case 2:
            if(i < 3) {
                __action__ = 0;
            }
            else {
                __action__ = 9;
            }
            break;

            case 4:
            painter.setPen(Qt::red);
            __action__ = 7;
            break;

            case 5:
            i++;
            x += 70;
            __action__ = 2;
            break;

            case 6:
            painter.setPen(Qt::black);
            painter.drawText(x + 50, 35, tr(":"));
            __action__ = 5;
            break;

            case 7:
            painter.drawText(x, 35, d.setNum(time[i] / 10));
            painter.drawText(x + 20, 35, d.setNum(time[i] % 10));
            __action__ = 1;
            break;

            case 8:
            f.setPointSize(30);
            f.setWeight(5);
            painter.setFont(f);
            __action__ = 2;
            break;

            case 9:
            return;
        }
    }
}
