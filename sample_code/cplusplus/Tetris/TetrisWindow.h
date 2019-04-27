
#ifndef TETRISWINDOW_H
#define TETRISWINDOW_H

#include <QWidget>
#include <QPushButton>
#include <QGridLayout>
#include <QApplication>

#include "all_definitions.h"

#include "PlayerWidget.h"

class TetrisWindow : public QWidget {
    Q_OBJECT

  private:
    QPushButton * startNewGameButton;
    QPushButton * exitButton;
    QPushButton * pauseButton;
    PlayerWidget * player;

    public slots:

    void start();
    public slots:

    void pause();

  public:

    ~TetrisWindow();

    TetrisWindow();

  protected:

    void keyPressEvent(QKeyEvent * e);
};

#endif
