
#ifndef ENGINE_H
#define ENGINE_H

#include "all_definitions.h"

#include "Block.h"
#include "PlayerWidget.h"
#include "Playground.h"

#include "__smbase/StateMachine.h"

class Engine {
  private:
    int clearedLines;
    static const int RIGHT = 1;
    int level;
    static const int LEFT = 2;
    static const int ROTATE = 3;
    int score;
    static const int DOWN = 0;
    int speed;
    Playground * playground;
    PlayerWidget * playerWidget;

  public:

    void pause();

    void start();

    void drop();

    void rotate();

    void down();

    void left();

    void right();

    Engine(PlayerWidget * w);

    ~Engine();

  private:

    bool isGameOver();

    void setNewGame();

    void draw();

    void move(int which);

    void setSpeed();

    void renew();

    bool isSettled();

    bool isValid(Block * b);

  private:

    class EngineStateMachine;
    friend class EngineStateMachine;

    EngineStateMachine *__mySM;

    static const int __Start = 0;
    static const int __Pause = 1;
    static const int __Drop = 2;
    static const int __GoRight = 3;
    static const int __Rotate = 4;
    static const int __GoLeft = 5;
    static const int __GoDown = 6;
    static const int __Gravity = 7;

    void __GoingRightEntry();
    void __InitializedEntry();
    void __OverEntry();
    void __DrawingEntry();
    void __RotatingEntry();
    void __HardFallingEntry();
    void __SoftFallingEntry();
    void __GoingLeftEntry();
    void __InMotionEntry();

    void __T_2Effect();
    void __T_24Effect();
    int __T_1When();
    bool __T_0Guard();
    void __T_7Effect();
    void __T_11Effect();
    bool __T_12Guard();
    bool __T_20Guard();

    class EngineStateMachine : public __smbase::StateMachine {
      private:
        __smbase::State *goingRight;
        __smbase::State *paused;
        __smbase::State *initialized;
        __smbase::State *over;
        __smbase::State *drawing;
        __smbase::State *rotating;
        __smbase::State *hardFalling;
        __smbase::State *softFalling;
        __smbase::State *goingLeft;
        __smbase::State *inMotion;
        __smbase::State *initialInMotion;
        __smbase::State *initialTop;
        __smbase::Transition *t_2;
        __smbase::Transition *t_8;
        __smbase::Transition *t_9;
        __smbase::Transition *t_10;
        __smbase::Transition *t_15;
        __smbase::Transition *t_16;
        __smbase::Transition *t_17;
        __smbase::Transition *t_19;
        __smbase::Transition *t_22;
        __smbase::Transition *t_24;
        __smbase::Transition *t_1;
        __smbase::Transition *t_0;
        __smbase::Transition *t_3;
        __smbase::Transition *t_4;
        __smbase::Transition *t_5;
        __smbase::Transition *t_6;
        __smbase::Transition *t_7;
        __smbase::Transition *t_11;
        __smbase::Transition *t_12;
        __smbase::Transition *t_13;
        __smbase::Transition *t_14;
        __smbase::Transition *t_18;
        __smbase::Transition *t_20;
        __smbase::Transition *t_21;
        __smbase::Transition *t_23;

      public:
        EngineStateMachine(void *c);
        ~EngineStateMachine();

      protected:
        void init();

      private:

        friend class GoingRight;

        class GoingRight : public __smbase::State { 

          public:
            GoingRight(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
        };

        friend class Paused;

        class Paused : public __smbase::State { 

          public:
            Paused(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void doActivity();
        };

        friend class Initialized;

        class Initialized : public __smbase::State { 

          public:
            Initialized(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
        };

        friend class Over;

        class Over : public __smbase::State { 

          public:
            Over(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
        };

        friend class Drawing;

        class Drawing : public __smbase::State { 

          public:
            Drawing(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
        };

        friend class Rotating;

        class Rotating : public __smbase::State { 

          public:
            Rotating(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
        };

        friend class HardFalling;

        class HardFalling : public __smbase::State { 

          public:
            HardFalling(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
        };

        friend class SoftFalling;

        class SoftFalling : public __smbase::State { 

          public:
            SoftFalling(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
        };

        friend class GoingLeft;

        class GoingLeft : public __smbase::State { 

          public:
            GoingLeft(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
        };

        friend class InMotion;

        class InMotion : public __smbase::State { 

          public:
            InMotion(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void exit();
        };

        friend class InitialInMotion;

        class InitialInMotion : public __smbase::State { 

          public:
            InitialInMotion(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void doActivity();
        };

        friend class InitialTop;

        class InitialTop : public __smbase::State { 

          public:
            InitialTop(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void doActivity();
        };

        friend class T_2;

        class T_2 : public __smbase::Transition {
          public:
            T_2(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_8;

        class T_8 : public __smbase::Transition {
          public:
            T_8(bool b, __smbase::StateMachine *);
        };

        friend class T_9;

        class T_9 : public __smbase::Transition {
          public:
            T_9(bool b, __smbase::StateMachine *);
        };

        friend class T_10;

        class T_10 : public __smbase::Transition {
          public:
            T_10(bool b, __smbase::StateMachine *);
        };

        friend class T_15;

        class T_15 : public __smbase::Transition {
          public:
            T_15(bool b, __smbase::StateMachine *);
        };

        friend class T_16;

        class T_16 : public __smbase::Transition {
          public:
            T_16(bool b, __smbase::StateMachine *);
        };

        friend class T_17;

        class T_17 : public __smbase::Transition {
          public:
            T_17(bool b, __smbase::StateMachine *);
        };

        friend class T_19;

        class T_19 : public __smbase::Transition {
          public:
            T_19(bool b, __smbase::StateMachine *);
        };

        friend class T_22;

        class T_22 : public __smbase::Transition {
          public:
            T_22(bool b, __smbase::StateMachine *);
        };

        friend class T_24;

        class T_24 : public __smbase::Transition {
          public:
            T_24(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_1;

        class T_1 : public __smbase::Transition {
          public:
            T_1(bool b, __smbase::StateMachine *);
        };

        friend class T_0;

        class T_0 : public __smbase::Transition {
          public:
            T_0(bool b, __smbase::StateMachine *);
        };

        friend class T_3;

        class T_3 : public __smbase::Transition {
          public:
            T_3(bool b, __smbase::StateMachine *);
        };

        friend class T_4;

        class T_4 : public __smbase::Transition {
          public:
            T_4(bool b, __smbase::StateMachine *);
        };

        friend class T_5;

        class T_5 : public __smbase::Transition {
          public:
            T_5(bool b, __smbase::StateMachine *);
        };

        friend class T_6;

        class T_6 : public __smbase::Transition {
          public:
            T_6(bool b, __smbase::StateMachine *);
        };

        friend class T_7;

        class T_7 : public __smbase::Transition {
          public:
            T_7(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_11;

        class T_11 : public __smbase::Transition {
          public:
            T_11(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_12;

        class T_12 : public __smbase::Transition {
          public:
            T_12(bool b, __smbase::StateMachine *);
        };

        friend class T_13;

        class T_13 : public __smbase::Transition {
          public:
            T_13(bool b, __smbase::StateMachine *);
        };

        friend class T_14;

        class T_14 : public __smbase::Transition {
          public:
            T_14(bool b, __smbase::StateMachine *);
        };

        friend class T_18;

        class T_18 : public __smbase::Transition {
          public:
            T_18(bool b, __smbase::StateMachine *);
        };

        friend class T_20;

        class T_20 : public __smbase::Transition {
          public:
            T_20(bool b, __smbase::StateMachine *);
        };

        friend class T_21;

        class T_21 : public __smbase::Transition {
          public:
            T_21(bool b, __smbase::StateMachine *);
        };

        friend class T_23;

        class T_23 : public __smbase::Transition {
          public:
            T_23(bool b, __smbase::StateMachine *);
        };
    };
};

#endif
