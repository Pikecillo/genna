
#include "NextWidget.h"

void NextWidget::paintEvent(QPaintEvent * e) {
    QFrame::paintEvent(e);
    const QColor orange(255, 127, 0);
    static const QColor colorTable[] = {Qt::black, Qt::magenta, Qt::green, Qt::cyan, orange, Qt::blue, Qt::red, Qt::yellow};
    int t = 2 * lineWidth() + midLineWidth(), *c, i, x, k;
    QPainter painter(this);

    int __action__ = 4;

    while(true) {
        switch(__action__) {
            case 0:
            if(nextBlock == 0) {
                __action__ = 7;
            }
            else {
                __action__ = 5;
            }
            break;

            case 1:
            if(i < 8) {
                __action__ = 3;
            }
            else {
                __action__ = 6;
            }
            break;

            case 3:
            painter.fillRect((c[i] - 3 + x) * 20 + t + 1, c[i + 1] * 20 + t + 1, 18, 18, colorTable[k]);
            i += 2;
            __action__ = 1;
            break;

            case 4:
            painter.fillRect(t, t, 120, 80, colorTable[0]);
            __action__ = 0;
            break;

            case 5:
            c = nextBlock->getCoordinates();
            k = nextBlock->getKind();
            x = k == Block::I || k == Block::O;
            i = 0;
            __action__ = 1;
            break;

            case 6:
            return;
            case 7:
            return;
        }
    }
}

void NextWidget::draw(Block * b) {
    nextBlock = b;
    update();
}

NextWidget::NextWidget() {
    int border;

    nextBlock = 0;

    setFrameStyle(QFrame::Box | QFrame::Raised);
    setLineWidth(4);
    setMidLineWidth(3);

    border = 4 * lineWidth() + 2 * midLineWidth();
    setFixedSize(120 + border, 80 + border);
}
