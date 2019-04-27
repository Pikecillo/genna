
#ifndef CLOCK_H
#define CLOCK_H

#include <QWidget>
#include <QPushButton>
#include <QGridLayout>

#include "all_definitions.h"

#include "DigitalDisplay.h"

#include "__smbase/StateMachine.h"

class Clock : public QWidget {
    Q_OBJECT

  private:
    int minutes;
    int seconds;
    int hours;
    DigitalDisplay * cDisplay;
    QPushButton * incr;
    QPushButton * decr;
    QPushButton * mode;

    public slots:

    void modeButton();
    public slots:

    void inc();
    public slots:

    void dec();

  public:

    Clock();

    ~Clock();

  private:

    class ClockStateMachine;
    friend class ClockStateMachine;

    ClockStateMachine *__mySM;

    static const int __ModeButton = 0;
    static const int __Increment = 1;
    static const int __Decrement = 2;
    static const int __AntiIdle = 3;
    static const int __Tick = 4;

    void __SetHoursEntry();
    void __DisplayingEntry();
    void __SetMinutesEntry();
    void __SetSecondsEntry();

    void __T_15Effect();
    void __T_3Effect();
    void __T_9Effect();
    void __T_10Effect();
    void __T_13Effect();
    void __T_16Effect();
    int __T_7When();
    int __T_4When();
    int __T_12When();
    void __T_14Effect();
    int __T_14When();

    class ClockStateMachine : public __smbase::StateMachine {
      private:
        __smbase::State *setHours;
        __smbase::State *displaying;
        __smbase::State *setMinutes;
        __smbase::State *setSeconds;
        __smbase::State *setting;
        __smbase::State *finalSettings;
        __smbase::State *settingInitial;
        __smbase::State *iTop;
        __smbase::Transition *t_0;
        __smbase::Transition *t_1;
        __smbase::Transition *t_15;
        __smbase::Transition *t_3;
        __smbase::Transition *t_5;
        __smbase::Transition *t_9;
        __smbase::Transition *t_10;
        __smbase::Transition *t_11;
        __smbase::Transition *t_13;
        __smbase::Transition *t_16;
        __smbase::Transition *t_7;
        __smbase::Transition *t_4;
        __smbase::Transition *t_12;
        __smbase::Transition *t_14;
        __smbase::Transition *t_2;
        __smbase::Transition *t_6;
        __smbase::Transition *t_8;

      public:
        ClockStateMachine(void *c);
        ~ClockStateMachine();

      protected:
        void init();

      private:

        friend class SetHours;

        class SetHours : public __smbase::State { 

          public:
            SetHours(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
            void exit();
        };

        friend class Displaying;

        class Displaying : public __smbase::State { 

          public:
            Displaying(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
            void exit();
        };

        friend class SetMinutes;

        class SetMinutes : public __smbase::State { 

          public:
            SetMinutes(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
            void exit();
        };

        friend class SetSeconds;

        class SetSeconds : public __smbase::State { 

          public:
            SetSeconds(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
            void doActivity();
            void exit();
        };

        friend class Setting;

        class Setting : public __smbase::State { 

          public:
            Setting(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void entry();
        };

        friend class FinalSettings;

        class FinalSettings : public __smbase::State { 

          public:
            FinalSettings(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void doActivity();
        };

        friend class SettingInitial;

        class SettingInitial : public __smbase::State { 

          public:
            SettingInitial(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void doActivity();
        };

        friend class ITop;

        class ITop : public __smbase::State { 

          public:
            ITop(__smbase::StateMachine *sm);
            __smbase::EventHandle *handleEvent(__smbase::Event *e);
            void doActivity();
        };

        friend class T_0;

        class T_0 : public __smbase::Transition {
          public:
            T_0(bool b, __smbase::StateMachine *);
        };

        friend class T_1;

        class T_1 : public __smbase::Transition {
          public:
            T_1(bool b, __smbase::StateMachine *);
        };

        friend class T_15;

        class T_15 : public __smbase::Transition {
          public:
            T_15(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_3;

        class T_3 : public __smbase::Transition {
          public:
            T_3(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_5;

        class T_5 : public __smbase::Transition {
          public:
            T_5(bool b, __smbase::StateMachine *);
        };

        friend class T_9;

        class T_9 : public __smbase::Transition {
          public:
            T_9(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_10;

        class T_10 : public __smbase::Transition {
          public:
            T_10(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_11;

        class T_11 : public __smbase::Transition {
          public:
            T_11(bool b, __smbase::StateMachine *);
        };

        friend class T_13;

        class T_13 : public __smbase::Transition {
          public:
            T_13(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_16;

        class T_16 : public __smbase::Transition {
          public:
            T_16(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_7;

        class T_7 : public __smbase::Transition {
          public:
            T_7(bool b, __smbase::StateMachine *);
        };

        friend class T_4;

        class T_4 : public __smbase::Transition {
          public:
            T_4(bool b, __smbase::StateMachine *);
        };

        friend class T_12;

        class T_12 : public __smbase::Transition {
          public:
            T_12(bool b, __smbase::StateMachine *);
        };

        friend class T_14;

        class T_14 : public __smbase::Transition {
          public:
            T_14(bool b, __smbase::StateMachine *);
            void executeEffect();
        };

        friend class T_2;

        class T_2 : public __smbase::Transition {
          public:
            T_2(bool b, __smbase::StateMachine *);
        };

        friend class T_6;

        class T_6 : public __smbase::Transition {
          public:
            T_6(bool b, __smbase::StateMachine *);
        };

        friend class T_8;

        class T_8 : public __smbase::Transition {
          public:
            T_8(bool b, __smbase::StateMachine *);
        };
    };
};

#endif
