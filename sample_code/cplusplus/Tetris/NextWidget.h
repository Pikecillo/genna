
#ifndef NEXTWIDGET_H
#define NEXTWIDGET_H

#include <QFrame>
#include <QWidget>
#include <QPaintEvent>
#include <QPainter>
#include <Qt>

#include "all_definitions.h"

#include "Block.h"

class NextWidget : public QFrame {
  private:
    Block * nextBlock;

  public:

    void paintEvent(QPaintEvent * e);

    void draw(Block * b);

    NextWidget();
};

#endif
