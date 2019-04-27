
#include "PlayerWidget.h"

Engine * PlayerWidget::getEngine() {
    return engine;
}

NextWidget * PlayerWidget::getNextWidget() {
    return myNextWidget;
}

void PlayerWidget::actualizeNumbers(int li, int sc, int le) {
    lines->display(li);
    score->display(sc);
    level->display(le);
}

PlayerWidget::PlayerWidget() {
    myPgWidget = new PlaygroundWidget();
    myNextWidget = new NextWidget();
    engine = new Engine(this);
    lines = new QLCDNumber(4, 0);
    score = new QLCDNumber(6, 0);
    level = new QLCDNumber(2, 0);
    linesLabel = new QLabel(tr("Lines"));
    scoreLabel = new QLabel(tr("Score"));
    levelLabel = new QLabel(tr("Level"));

    QGridLayout *layout = new QGridLayout;

    layout->addWidget(myPgWidget, 0, 0, 7, 1);
    layout->addWidget(myNextWidget, 0, 1);
    layout->addWidget(linesLabel, 1, 1);
    layout->addWidget(lines, 2, 1);
    layout->addWidget(scoreLabel, 3, 1);
    layout->addWidget(score, 4, 1);
    layout->addWidget(levelLabel, 5, 1);
    layout->addWidget(level, 6, 1);

    setLayout(layout);

    resize(300, 500);
}

PlaygroundWidget * PlayerWidget::getPlaygroundWidget() {
    return myPgWidget;
}
