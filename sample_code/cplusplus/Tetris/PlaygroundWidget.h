
#ifndef PLAYGROUNDWIDGET_H
#define PLAYGROUNDWIDGET_H

#include <QFrame>
#include <QWidget>
#include <QPaintEvent>
#include <QPainter>
#include <Qt>

#include "all_definitions.h"

#include "Playground.h"

class PlaygroundWidget : public QFrame {
  private:
    Playground * myPlayground;

  public:

    void paintEvent(QPaintEvent * e);

    PlaygroundWidget();

    void draw(Playground * pg);
};

#endif
