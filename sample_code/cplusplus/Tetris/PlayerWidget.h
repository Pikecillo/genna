
#ifndef PLAYERWIDGET_H
#define PLAYERWIDGET_H

#include <QWidget>
#include <QGridLayout>
#include <QLabel>
#include <QLCDNumber>

#include "all_definitions.h"

#include "Engine.h"
#include "NextWidget.h"
#include "PlaygroundWidget.h"

class PlayerWidget : public QWidget {
  private:
    QLCDNumber * lines;
    QLabel * levelLabel;
    QLCDNumber * level;
    QLCDNumber * score;
    QLabel * linesLabel;
    QLabel * scoreLabel;
    Engine * engine;
    PlaygroundWidget * myPgWidget;
    NextWidget * myNextWidget;

  public:

    Engine * getEngine();

    NextWidget * getNextWidget();

    void actualizeNumbers(int li, int sc, int le);

    PlayerWidget();

    PlaygroundWidget * getPlaygroundWidget();
};

#endif
