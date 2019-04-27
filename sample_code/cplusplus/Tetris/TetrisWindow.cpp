
#include "TetrisWindow.h"

void TetrisWindow::start() {
    player->getEngine()->start();
}

TetrisWindow::~TetrisWindow() {
    delete startNewGameButton;
    delete pauseButton;
    delete exitButton;
}

void TetrisWindow::pause() {
    player->getEngine()->pause();
}

TetrisWindow::TetrisWindow() {
    player = new PlayerWidget();

    startNewGameButton = new QPushButton(tr("&NewGame"));
    pauseButton = new QPushButton(tr("&Pause"));
    exitButton = new QPushButton(tr("&ExitTetris"));

    QGridLayout *layout = new QGridLayout();

    startNewGameButton->setFocusPolicy(Qt::NoFocus);
    pauseButton->setFocusPolicy(Qt::NoFocus);
    exitButton->setFocusPolicy(Qt::NoFocus);

    connect(startNewGameButton, SIGNAL(clicked()), this, SLOT(start()));
    connect(exitButton, SIGNAL(clicked()), QApplication::instance(), SLOT(quit()));
    connect(pauseButton, SIGNAL(clicked()), this, SLOT(pause()));

    layout->addWidget(player, 0, 0, 1, 3);
    layout->addWidget(startNewGameButton, 1, 0);
    layout->addWidget(pauseButton, 1, 1);
    layout->addWidget(exitButton, 1, 2);
    setLayout(layout);
    setWindowTitle(tr("Tetris"));
}

void TetrisWindow::keyPressEvent(QKeyEvent * e) {
    int __action__ = 0;

    while(true) {
        switch(__action__) {
            case 0:
            if(e->key() == Qt::Key_Up) {
                __action__ = 2;
            }
            else if(e->key() == Qt::Key_Down) {
                __action__ = 3;
            }
            else if(e->key() == Qt::Key_Right) {
                __action__ = 4;
            }
            else if(e->key() == Qt::Key_Left) {
                __action__ = 5;
            }
            else if(e->key() == Qt::Key_Space) {
                __action__ = 6;
            }
            else {
                __action__ = 7;
            }
            break;

            case 2:
            player->getEngine()->rotate();
            __action__ = 8;
            break;

            case 3:
            player->getEngine()->down();
            __action__ = 8;
            break;

            case 4:
            player->getEngine()->right();
            __action__ = 8;
            break;

            case 5:
            player->getEngine()->left();
            __action__ = 8;
            break;

            case 6:
            player->getEngine()->drop();
            __action__ = 8;
            break;

            case 7:
            return;
            case 8:
            return;
        }
    }
}
