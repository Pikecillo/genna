
#include "Clock.h"

Clock::Clock() {
    hours = 0;
    minutes = 0;
    seconds = 0;

    cDisplay = new DigitalDisplay();
    mode = new QPushButton("Mode");
    incr = new QPushButton("Inc");
    decr = new QPushButton("Dec");

    connect(mode, SIGNAL(clicked()), this, SLOT(modeButton()));
    connect(incr, SIGNAL(clicked()), this, SLOT(inc()));
    connect(decr, SIGNAL(clicked()), this, SLOT(dec()));

    QGridLayout *layout = new QGridLayout;

    layout->addWidget(cDisplay, 0, 0, 1, 3);
    layout->addWidget(mode, 1, 0, 1, 1);
    layout->addWidget(incr, 1, 1, 1, 1);
    layout->addWidget(decr, 1, 2, 1, 1);

    setLayout(layout);

    setWindowTitle("Digital Clock");
    __mySM = new ClockStateMachine(this);
}

void Clock::modeButton() {
    __mySM->postEvent(new __smbase::Event(__ModeButton));
}

void Clock::inc() {
    __mySM->postEvent(new __smbase::Event(__Increment));
}

void Clock::dec() {
    __mySM->postEvent(new __smbase::Event(__Decrement));
}

Clock::~Clock() {
    delete cDisplay;
    delete incr;
    delete decr;
    delete mode;
    delete __mySM;
}

void Clock::__SetHoursEntry() {
    cDisplay->show(hours, minutes, seconds, DigitalDisplay::H);
}

void Clock::__DisplayingEntry() {
    cDisplay->show(hours, minutes, seconds, DigitalDisplay::NONE);
}

void Clock::__SetMinutesEntry() {
    cDisplay->show(hours, minutes, seconds, DigitalDisplay::M);
}

void Clock::__SetSecondsEntry() {
    cDisplay->show(hours, minutes, seconds, DigitalDisplay::S);
}

void Clock::__T_15Effect() {
    hours = (hours + 1) % 24;
}

void Clock::__T_3Effect() {
    hours = (hours + 23) % 24;
}

void Clock::__T_9Effect() {
    minutes = (minutes + 59) % 60;
}

void Clock::__T_10Effect() {
    seconds = (seconds + 1) % 60;
}

void Clock::__T_13Effect() {
    seconds = (seconds + 59) % 60;
}

void Clock::__T_16Effect() {
    minutes = (minutes + 1) % 60;
}

int Clock::__T_7When() {
    return 10000;
}

int Clock::__T_4When() {
    return 10000;
}

int Clock::__T_12When() {
    return 10000;
}

void Clock::__T_14Effect() {
    seconds = ++seconds % 60;
    minutes = seconds == 0 ? ++minutes % 60 : minutes;
    hours = (minutes == 0 && seconds == 0) ? ++hours % 24 : hours;
}

int Clock::__T_14When() {
    return 1000;
}

Clock::ClockStateMachine::ClockStateMachine(void *c) : __smbase::StateMachine(c) { }

Clock::ClockStateMachine::~ClockStateMachine() {
    delete setting;
    delete setHours;
    delete displaying;
    delete setMinutes;
    delete setSeconds;
    delete finalSettings;
    delete settingInitial;
    delete iTop;
    delete t_0;
    delete t_1;
    delete t_15;
    delete t_3;
    delete t_5;
    delete t_9;
    delete t_10;
    delete t_11;
    delete t_13;
    delete t_16;
    delete t_7;
    delete t_4;
    delete t_12;
    delete t_14;
    delete t_2;
    delete t_6;
    delete t_8;
    postEvent(new __smbase::Event(__smbase::StateMachine::DIE));
    this->wait();
}

void Clock::ClockStateMachine::init() {
    setting = new Setting(this);
    setHours = new SetHours(this);
    displaying = new Displaying(this);
    setMinutes = new SetMinutes(this);
    setSeconds = new SetSeconds(this);
    finalSettings = new FinalSettings(this);
    settingInitial = new SettingInitial(this);
    iTop = new ITop(this);
    t_0 = new T_0(false, this);
    t_1 = new T_1(false, this);
    t_15 = new T_15(true, this);
    t_3 = new T_3(true, this);
    t_5 = new T_5(false, this);
    t_9 = new T_9(true, this);
    t_10 = new T_10(true, this);
    t_11 = new T_11(false, this);
    t_13 = new T_13(true, this);
    t_16 = new T_16(true, this);
    t_7 = new T_7(false, this);
    t_4 = new T_4(false, this);
    t_12 = new T_12(false, this);
    t_14 = new T_14(true, this);
    t_2 = new T_2(false, this);
    t_6 = new T_6(false, this);
    t_8 = new T_8(false, this);

    setting->setDirectAncestor(top);
    setHours->setDirectAncestor(setting);
    displaying->setDirectAncestor(top);
    setMinutes->setDirectAncestor(setting);
    setSeconds->setDirectAncestor(setting);
    finalSettings->setDirectAncestor(setting);
    settingInitial->setDirectAncestor(setting);
    iTop->setDirectAncestor(top);

    innermostActive = iTop;
}

Clock::ClockStateMachine::SetHours::SetHours(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Clock::ClockStateMachine::SetHours::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Clock::__Decrement:

        transitionSequence.push_back(sm->t_3);
        handle = new __smbase::EventHandle(transitionSequence, sm->setHours);
        break;

        case Clock::__ModeButton:

        transitionSequence.push_back(sm->t_0);
        handle = new __smbase::EventHandle(transitionSequence, sm->setMinutes);
        break;

        case Clock::__AntiIdle:
        if(isWaited(e)) {
            transitionSequence.push_back(sm->t_12);
            handle = new __smbase::EventHandle(transitionSequence, sm->finalSettings);
            removeWaited(e);
        }
        break;

        case Clock::__Increment:

        transitionSequence.push_back(sm->t_15);
        handle = new __smbase::EventHandle(transitionSequence, sm->setHours);
        break;
    }
    return handle;
}

void Clock::ClockStateMachine::SetHours::entry() {
    __smbase::Event *e;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    Clock *context = static_cast<Clock *>(sm->context);

    context->__SetHoursEntry();

    e = new __smbase::Event(Clock::__AntiIdle);
    addWaited(e);
    sm->postTimeEvent(e, context->__T_12When());
}

void Clock::ClockStateMachine::SetHours::doActivity() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

void Clock::ClockStateMachine::SetHours::exit() {
    clearWaited();
}

Clock::ClockStateMachine::Displaying::Displaying(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Clock::ClockStateMachine::Displaying::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Clock::__Tick:
        if(isWaited(e)) {
            transitionSequence.push_back(sm->t_14);
            handle = new __smbase::EventHandle(transitionSequence, sm->displaying);
            removeWaited(e);
        }
        break;

        case Clock::__ModeButton:

        transitionSequence.push_back(sm->t_1);
        handle = new __smbase::EventHandle(transitionSequence, sm->setting);
        break;
    }
    return handle;
}

void Clock::ClockStateMachine::Displaying::entry() {
    __smbase::Event *e;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    Clock *context = static_cast<Clock *>(sm->context);

    context->__DisplayingEntry();

    e = new __smbase::Event(Clock::__Tick);
    addWaited(e);
    sm->postTimeEvent(e, context->__T_14When());
}

void Clock::ClockStateMachine::Displaying::doActivity() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

void Clock::ClockStateMachine::Displaying::exit() {
    clearWaited();
}

Clock::ClockStateMachine::SetMinutes::SetMinutes(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Clock::ClockStateMachine::SetMinutes::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Clock::__Decrement:

        transitionSequence.push_back(sm->t_9);
        handle = new __smbase::EventHandle(transitionSequence, sm->setMinutes);
        break;

        case Clock::__ModeButton:

        transitionSequence.push_back(sm->t_5);
        handle = new __smbase::EventHandle(transitionSequence, sm->setSeconds);
        break;

        case Clock::__AntiIdle:
        if(isWaited(e)) {
            transitionSequence.push_back(sm->t_7);
            handle = new __smbase::EventHandle(transitionSequence, sm->finalSettings);
            removeWaited(e);
        }
        break;

        case Clock::__Increment:

        transitionSequence.push_back(sm->t_16);
        handle = new __smbase::EventHandle(transitionSequence, sm->setMinutes);
        break;
    }
    return handle;
}

void Clock::ClockStateMachine::SetMinutes::entry() {
    __smbase::Event *e;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    Clock *context = static_cast<Clock *>(sm->context);

    context->__SetMinutesEntry();

    e = new __smbase::Event(Clock::__AntiIdle);
    addWaited(e);
    sm->postTimeEvent(e, context->__T_7When());
}

void Clock::ClockStateMachine::SetMinutes::doActivity() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

void Clock::ClockStateMachine::SetMinutes::exit() {
    clearWaited();
}

Clock::ClockStateMachine::SetSeconds::SetSeconds(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Clock::ClockStateMachine::SetSeconds::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Clock::__Decrement:

        transitionSequence.push_back(sm->t_13);
        handle = new __smbase::EventHandle(transitionSequence, sm->setSeconds);
        break;

        case Clock::__ModeButton:

        transitionSequence.push_back(sm->t_11);
        handle = new __smbase::EventHandle(transitionSequence, sm->displaying);
        break;

        case Clock::__AntiIdle:
        if(isWaited(e)) {
            transitionSequence.push_back(sm->t_4);
            handle = new __smbase::EventHandle(transitionSequence, sm->finalSettings);
            removeWaited(e);
        }
        break;

        case Clock::__Increment:

        transitionSequence.push_back(sm->t_10);
        handle = new __smbase::EventHandle(transitionSequence, sm->setSeconds);
        break;
    }
    return handle;
}

void Clock::ClockStateMachine::SetSeconds::entry() {
    __smbase::Event *e;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    Clock *context = static_cast<Clock *>(sm->context);

    context->__SetSecondsEntry();

    e = new __smbase::Event(Clock::__AntiIdle);
    addWaited(e);
    sm->postTimeEvent(e, context->__T_4When());
}

void Clock::ClockStateMachine::SetSeconds::doActivity() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

void Clock::ClockStateMachine::SetSeconds::exit() {
    clearWaited();
}

Clock::ClockStateMachine::Setting::Setting(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Clock::ClockStateMachine::Setting::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETED:

        transitionSequence.push_back(sm->t_2);
        handle = new __smbase::EventHandle(transitionSequence, sm->displaying);
        break;
    }
    return handle;
}

void Clock::ClockStateMachine::Setting::entry() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);

    if(this == stateMachine->getInnermostActive()) {
        stateMachine->setInnermostActive(sm->settingInitial);
    }
}

Clock::ClockStateMachine::FinalSettings::FinalSettings(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Clock::ClockStateMachine::FinalSettings::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    return handle;
}

void Clock::ClockStateMachine::FinalSettings::doActivity() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETED));
}

Clock::ClockStateMachine::SettingInitial::SettingInitial(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Clock::ClockStateMachine::SettingInitial::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_6);
        handle = new __smbase::EventHandle(transitionSequence, sm->setHours);
        break;
    }
    return handle;
}

void Clock::ClockStateMachine::SettingInitial::doActivity() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Clock::ClockStateMachine::ITop::ITop(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Clock::ClockStateMachine::ITop::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_8);
        handle = new __smbase::EventHandle(transitionSequence, sm->displaying);
        break;
    }
    return handle;
}

void Clock::ClockStateMachine::ITop::doActivity() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Clock::ClockStateMachine::T_0::T_0(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_1::T_1(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_15::T_15(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Clock::ClockStateMachine::T_15::executeEffect() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    static_cast<Clock *>(sm->context)->__T_15Effect();
}

Clock::ClockStateMachine::T_3::T_3(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Clock::ClockStateMachine::T_3::executeEffect() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    static_cast<Clock *>(sm->context)->__T_3Effect();
}

Clock::ClockStateMachine::T_5::T_5(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_9::T_9(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Clock::ClockStateMachine::T_9::executeEffect() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    static_cast<Clock *>(sm->context)->__T_9Effect();
}

Clock::ClockStateMachine::T_10::T_10(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Clock::ClockStateMachine::T_10::executeEffect() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    static_cast<Clock *>(sm->context)->__T_10Effect();
}

Clock::ClockStateMachine::T_11::T_11(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_13::T_13(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Clock::ClockStateMachine::T_13::executeEffect() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    static_cast<Clock *>(sm->context)->__T_13Effect();
}

Clock::ClockStateMachine::T_16::T_16(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Clock::ClockStateMachine::T_16::executeEffect() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    static_cast<Clock *>(sm->context)->__T_16Effect();
}

Clock::ClockStateMachine::T_7::T_7(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_4::T_4(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_12::T_12(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_14::T_14(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Clock::ClockStateMachine::T_14::executeEffect() {
    ClockStateMachine *sm = static_cast<ClockStateMachine *>(stateMachine);
    static_cast<Clock *>(sm->context)->__T_14Effect();
}

Clock::ClockStateMachine::T_2::T_2(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_6::T_6(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Clock::ClockStateMachine::T_8::T_8(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }
