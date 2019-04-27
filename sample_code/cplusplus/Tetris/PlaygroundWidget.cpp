
#include "PlaygroundWidget.h"

void PlaygroundWidget::paintEvent(QPaintEvent * e) {
    QFrame::paintEvent(e);
    const QColor orange(255, 127, 0);
    QColor color;
    static const QColor colorTable[] = {Qt::black, Qt::magenta, Qt::green, Qt::cyan, orange, Qt::blue, Qt::red, Qt::yellow};
    int t = 2 * lineWidth() + midLineWidth(), *c, **s, i, j;
    QPainter painter(this);

    int __action__ = 9;

    while(true) {
        switch(__action__) {
            case 0:
            if(j < 10) {
                __action__ = 6;
            }
            else {
                __action__ = 5;
            }
            break;

            case 1:
            if(j < 8) {
                __action__ = 8;
            }
            else {
                __action__ = 10;
            }
            break;

            case 2:
            if(myPlayground == 0) {
                __action__ = 11;
            }
            else {
                __action__ = 7;
            }
            break;

            case 3:
            if(i < 21) {
                __action__ = 0;
            }
            else {
                __action__ = 1;
            }
            break;

            case 5:
            i++;
            j = 0;
            __action__ = 3;
            break;

            case 6:
            color = colorTable[s[i][j]];
            painter.fillRect(j * 20 + 1 + t, i * 20 + 1 + t, 18, 18, color);
            j++;
            __action__ = 0;
            break;

            case 7:
            c = myPlayground->getActual()->getCoordinates();
            s = myPlayground->getSpace();
            i = 0;
            j = 0;
            __action__ = 3;
            break;

            case 8:
            color = colorTable[myPlayground->getActual()->getKind()];
            painter.fillRect(c[j] * 20 + 1 + t, c[j + 1] * 20 + 1 + t, 18, 18, color);
            j += 2;
            __action__ = 1;
            break;

            case 9:
            painter.fillRect(t, t, 200, 420, colorTable[0]);
            painter.setPen(Qt::white);
            painter.drawLine(t, t + 59, t + 200, t + 59);
            painter.drawLine(t, t + 60, t + 200, t + 60);
            __action__ = 2;
            break;

            case 10:
            return;
            case 11:
            return;
        }
    }
}

PlaygroundWidget::PlaygroundWidget() {
    int border;

    myPlayground = 0;

    setFrameStyle(QFrame::Box | QFrame::Raised);
    setLineWidth(4);
    setMidLineWidth(3);

    border = 4 * lineWidth() + 2 * midLineWidth();
    setFixedSize(200 + border, 420 + border);
}

void PlaygroundWidget::draw(Playground * pg) {
    myPlayground = pg;
    update();
}
