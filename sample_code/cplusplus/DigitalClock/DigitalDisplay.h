
#ifndef DIGITALDISPLAY_H
#define DIGITALDISPLAY_H

#include <QLCDNumber>
#include <QPainter>
#include <QPaintEvent>

#include "all_definitions.h"

class DigitalDisplay : public QFrame {
  public:
    static const int H = 0;
    static const int M = 1;
    static const int NONE = -1;
    static const int S = 2;

  private:
    int which;
    int time [3];

  public:

    DigitalDisplay();

    void show(int h, int m, int s, int high);

  protected:

    void paintEvent(QPaintEvent * e);
};

#endif
