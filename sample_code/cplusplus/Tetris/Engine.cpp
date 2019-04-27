
#include "Engine.h"

void Engine::pause() {
    __mySM->postEvent(new __smbase::Event(__Pause));
}

void Engine::start() {
    __mySM->postEvent(new __smbase::Event(__Start));
}

void Engine::drop() {
    __mySM->postEvent(new __smbase::Event(__Drop));
}

void Engine::rotate() {
    __mySM->postEvent(new __smbase::Event(__Rotate));
}

void Engine::down() {
    __mySM->postEvent(new __smbase::Event(__GoDown));
}

void Engine::left() {
    __mySM->postEvent(new __smbase::Event(__GoLeft));
}

void Engine::right() {
    __mySM->postEvent(new __smbase::Event(__GoRight));
}

Engine::Engine(PlayerWidget * w) {
    playerWidget = w;
    playground = 0;
    __mySM = new EngineStateMachine(this);
}

Engine::~Engine() {
    delete __mySM;
}

bool Engine::isGameOver() {
    int *c = playground->getActual()->getCoordinates(), i = 0;

    int __action__ = 1;

    while(true) {
        switch(__action__) {
            case 0:
            if(c[i + 1] < 3) {
                __action__ = 5;
            }
            else {
                __action__ = 3;
            }
            break;

            case 1:
            if(i < 8) {
                __action__ = 0;
            }
            else {
                __action__ = 4;
            }
            break;

            case 3:
            i += 2;
            __action__ = 1;
            break;

            case 4:
            return false;
            case 5:
            return true;
        }
    }
}

void Engine::setNewGame() {
    int __action__ = 0;

    while(true) {
        switch(__action__) {
            case 0:
            if(playground != 0) {
                __action__ = 2;
            }
            else {
                __action__ = 3;
            }
            break;

            case 2:
            delete playground;
            __action__ = 3;
            break;

            case 3:
            playground = new Playground();
            speed = 1000;
            clearedLines = 0;
            score = 0;
            level = 1;
            __action__ = 4;
            break;

            case 4:
            return;
        }
    }
}

void Engine::draw() {
    playerWidget->getPlaygroundWidget()->draw(playground);
    playerWidget->getNextWidget()->draw(playground->getNext());
    playerWidget->actualizeNumbers(clearedLines, score, level);
}

void Engine::move(int which) {
    Block *b = playground->getActual(), *moved;

    int __action__ = 2;

    while(true) {
        switch(__action__) {
            case 0:
            if(isValid(moved)) {
                __action__ = 8;
            }
            else {
                __action__ = 7;
            }
            break;

            case 2:
            if(which ==DOWN) {
                __action__ = 4;
            }
            else if(which == ROTATE) {
                __action__ = 3;
            }
            else if(which == LEFT) {
                __action__ = 6;
            }
            else if(which == RIGHT) {
                __action__ = 5;
            }
            break;

            case 3:
            moved = new Block(b->rotate());
            __action__ = 0;
            break;

            case 4:
            moved = new Block(b->moveDown());
            __action__ = 0;
            break;

            case 5:
            moved = new Block(b->moveRight());
            __action__ = 0;
            break;

            case 6:
            moved = new Block(b->moveLeft());
            __action__ = 0;
            break;

            case 7:
            delete moved;
            __action__ = 9;
            break;

            case 8:
            playground->setActual(moved);
            __action__ = 9;
            break;

            case 9:
            return;
        }
    }
}

void Engine::setSpeed() {
    int i = 0, l[] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
    int spe[] = {1000, 900, 800, 700, 500, 300, 200, 100, 50, 25};

    int __action__ = 1;

    while(true) {
        switch(__action__) {
            case 1:
            if(i < 10) {
                __action__ = 2;
            }
            else {
                __action__ = 5;
            }
            break;

            case 2:
            if(clearedLines < l[i]) {
                __action__ = 3;
            }
            else {
                __action__ = 4;
            }
            break;

            case 3:
            speed = spe[i];
            level = i + 1;
            __action__ = 5;
            break;

            case 4:
            i++;
            __action__ = 1;
            break;

            case 5:
            return;
        }
    }
}

void Engine::renew() {
    int clearedNow;

    playground->settle();
    clearedNow = playground->clearLines();
    clearedLines += clearedNow;
    score += (10 + (clearedNow * clearedNow) * 100);
    setSpeed();
    playerWidget->actualizeNumbers(clearedLines, score, level);
}

bool Engine::isSettled() {
    int *c = playground->getActual()->getCoordinates(), **s = playground->getSpace(), i = 0;

    int __action__ = 1;

    while(true) {
        switch(__action__) {
            case 1:
            if(i < 8) {
                __action__ = 2;
            }
            else {
                __action__ = 4;
            }
            break;

            case 2:
            if(c[i + 1] == 20 || s[c[i + 1] + 1][c[i]] != Block::VOID) {
                __action__ = 5;
            }
            else {
                __action__ = 3;
            }
            break;

            case 3:
            i += 2;
            __action__ = 1;
            break;

            case 4:
            return false;
            case 5:
            return true;
        }
    }
}

bool Engine::isValid(Block * b) {
    int *c = b->getCoordinates(), **s = playground->getSpace(), i = 0;

    int __action__ = 2;

    while(true) {
        switch(__action__) {
            case 0:
            if(c[i] < 0 || c[i] > 9 || c[i + 1] < 0 || c[i + 1] > 20 || s[c[i + 1]][c[i]] != Block::VOID) {
                __action__ = 4;
            }
            else {
                __action__ = 3;
            }
            break;

            case 2:
            if(i < 8) {
                __action__ = 0;
            }
            else {
                __action__ = 5;
            }
            break;

            case 3:
            i += 2;
            __action__ = 2;
            break;

            case 4:
            return false;
            case 5:
            return true;
        }
    }
}

void Engine::__GoingRightEntry() {
    move(RIGHT);
}

void Engine::__InitializedEntry() {
    setNewGame();
}

void Engine::__OverEntry() {
    draw();
}

void Engine::__DrawingEntry() {
    draw();
}

void Engine::__RotatingEntry() {
    move(ROTATE);
}

void Engine::__HardFallingEntry() {
    move(DOWN);
}

void Engine::__SoftFallingEntry() {
    move(DOWN);
}

void Engine::__GoingLeftEntry() {
    move(LEFT);
}

void Engine::__InMotionEntry() {
    setSpeed();
}

void Engine::__T_2Effect() {
    setNewGame();
}

void Engine::__T_24Effect() {
    setNewGame();
}

int Engine::__T_1When() {
    return speed;
}

bool Engine::__T_0Guard() {
    return(isGameOver());
}

void Engine::__T_7Effect() {
    move(DOWN);
}

void Engine::__T_11Effect() {
    renew();
}

bool Engine::__T_12Guard() {
    return(isSettled());
}

bool Engine::__T_20Guard() {
    return(isSettled());
}

Engine::EngineStateMachine::EngineStateMachine(void *c) : __smbase::StateMachine(c) { }

Engine::EngineStateMachine::~EngineStateMachine() {
    delete inMotion;
    delete goingRight;
    delete paused;
    delete initialized;
    delete over;
    delete drawing;
    delete rotating;
    delete hardFalling;
    delete softFalling;
    delete goingLeft;
    delete initialInMotion;
    delete initialTop;
    delete t_2;
    delete t_8;
    delete t_9;
    delete t_10;
    delete t_15;
    delete t_16;
    delete t_17;
    delete t_19;
    delete t_22;
    delete t_24;
    delete t_1;
    delete t_0;
    delete t_3;
    delete t_4;
    delete t_5;
    delete t_6;
    delete t_7;
    delete t_11;
    delete t_12;
    delete t_13;
    delete t_14;
    delete t_18;
    delete t_20;
    delete t_21;
    delete t_23;
    postEvent(new __smbase::Event(__smbase::StateMachine::DIE));
    this->wait();
}

void Engine::EngineStateMachine::init() {
    inMotion = new InMotion(this);
    goingRight = new GoingRight(this);
    paused = new Paused(this);
    initialized = new Initialized(this);
    over = new Over(this);
    drawing = new Drawing(this);
    rotating = new Rotating(this);
    hardFalling = new HardFalling(this);
    softFalling = new SoftFalling(this);
    goingLeft = new GoingLeft(this);
    initialInMotion = new InitialInMotion(this);
    initialTop = new InitialTop(this);
    t_2 = new T_2(true, this);
    t_8 = new T_8(false, this);
    t_9 = new T_9(false, this);
    t_10 = new T_10(false, this);
    t_15 = new T_15(false, this);
    t_16 = new T_16(false, this);
    t_17 = new T_17(false, this);
    t_19 = new T_19(false, this);
    t_22 = new T_22(false, this);
    t_24 = new T_24(true, this);
    t_1 = new T_1(false, this);
    t_0 = new T_0(false, this);
    t_3 = new T_3(false, this);
    t_4 = new T_4(false, this);
    t_5 = new T_5(false, this);
    t_6 = new T_6(false, this);
    t_7 = new T_7(true, this);
    t_11 = new T_11(true, this);
    t_12 = new T_12(false, this);
    t_13 = new T_13(false, this);
    t_14 = new T_14(false, this);
    t_18 = new T_18(false, this);
    t_20 = new T_20(false, this);
    t_21 = new T_21(false, this);
    t_23 = new T_23(false, this);

    inMotion->setDirectAncestor(top);
    goingRight->setDirectAncestor(inMotion);
    paused->setDirectAncestor(top);
    initialized->setDirectAncestor(top);
    over->setDirectAncestor(top);
    drawing->setDirectAncestor(inMotion);
    rotating->setDirectAncestor(inMotion);
    hardFalling->setDirectAncestor(inMotion);
    softFalling->setDirectAncestor(inMotion);
    goingLeft->setDirectAncestor(inMotion);
    initialInMotion->setDirectAncestor(inMotion);
    initialTop->setDirectAncestor(top);

    innermostActive = initialTop;
}

Engine::EngineStateMachine::GoingRight::GoingRight(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::GoingRight::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_5);

        transitionSequence.push_back(sm->t_18);
        handle = new __smbase::EventHandle(transitionSequence, sm->drawing);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::GoingRight::entry() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__GoingRightEntry();
}

void Engine::EngineStateMachine::GoingRight::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::Paused::Paused(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::Paused::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Engine::__Start:

        transitionSequence.push_back(sm->t_24);
        handle = new __smbase::EventHandle(transitionSequence, sm->inMotion);
        break;

        case Engine::__Pause:

        transitionSequence.push_back(sm->t_10);
        handle = new __smbase::EventHandle(transitionSequence, sm->inMotion);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::Paused::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::Initialized::Initialized(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::Initialized::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Engine::__Start:

        transitionSequence.push_back(sm->t_8);
        handle = new __smbase::EventHandle(transitionSequence, sm->inMotion);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::Initialized::entry() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__InitializedEntry();
}

void Engine::EngineStateMachine::Initialized::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::Over::Over(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::Over::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Engine::__Start:

        transitionSequence.push_back(sm->t_2);
        handle = new __smbase::EventHandle(transitionSequence, sm->inMotion);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::Over::entry() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__OverEntry();
}

void Engine::EngineStateMachine::Over::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::Drawing::Drawing(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::Drawing::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Engine::__GoDown:

        transitionSequence.push_back(sm->t_22);
        handle = new __smbase::EventHandle(transitionSequence, sm->softFalling);
        break;

        case Engine::__Drop:

        transitionSequence.push_back(sm->t_15);
        handle = new __smbase::EventHandle(transitionSequence, sm->hardFalling);
        break;

        case Engine::__GoRight:

        transitionSequence.push_back(sm->t_16);
        handle = new __smbase::EventHandle(transitionSequence, sm->goingRight);
        break;

        case Engine::__Rotate:

        transitionSequence.push_back(sm->t_17);
        handle = new __smbase::EventHandle(transitionSequence, sm->rotating);
        break;

        case Engine::__GoLeft:

        transitionSequence.push_back(sm->t_19);
        handle = new __smbase::EventHandle(transitionSequence, sm->goingLeft);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::Drawing::entry() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__DrawingEntry();
}

void Engine::EngineStateMachine::Drawing::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::Rotating::Rotating(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::Rotating::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_6);

        transitionSequence.push_back(sm->t_18);
        handle = new __smbase::EventHandle(transitionSequence, sm->drawing);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::Rotating::entry() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__RotatingEntry();
}

void Engine::EngineStateMachine::Rotating::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::HardFalling::HardFalling(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::HardFalling::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_21);

        if(static_cast<Engine *>(sm->context)->__T_12Guard()) {
            transitionSequence.push_back(sm->t_12);

            if(static_cast<Engine *>(sm->context)->__T_0Guard()) {
                transitionSequence.push_back(sm->t_0);
                handle = new __smbase::EventHandle(transitionSequence, sm->over);
            }
            else {
                transitionSequence.push_back(sm->t_11);
                handle = new __smbase::EventHandle(transitionSequence, sm->inMotion);
            }
        }
        else {
            transitionSequence.push_back(sm->t_14);
            handle = new __smbase::EventHandle(transitionSequence, sm->hardFalling);
        }
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::HardFalling::entry() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__HardFallingEntry();
}

void Engine::EngineStateMachine::HardFalling::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::SoftFalling::SoftFalling(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::SoftFalling::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_23);
        handle = new __smbase::EventHandle(transitionSequence, sm->drawing);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::SoftFalling::entry() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__SoftFallingEntry();
}

void Engine::EngineStateMachine::SoftFalling::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::GoingLeft::GoingLeft(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::GoingLeft::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_4);

        transitionSequence.push_back(sm->t_18);
        handle = new __smbase::EventHandle(transitionSequence, sm->drawing);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::GoingLeft::entry() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__GoingLeftEntry();
}

void Engine::EngineStateMachine::GoingLeft::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::InMotion::InMotion(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::InMotion::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case Engine::__Pause:

        transitionSequence.push_back(sm->t_9);
        handle = new __smbase::EventHandle(transitionSequence, sm->paused);
        break;

        case Engine::__Gravity:
        if(isWaited(e)) {
            transitionSequence.push_back(sm->t_1);

            if(static_cast<Engine *>(sm->context)->__T_20Guard()) {
                transitionSequence.push_back(sm->t_20);

                if(static_cast<Engine *>(sm->context)->__T_0Guard()) {
                    transitionSequence.push_back(sm->t_0);
                    handle = new __smbase::EventHandle(transitionSequence, sm->over);
                }
                else {
                    transitionSequence.push_back(sm->t_11);
                    handle = new __smbase::EventHandle(transitionSequence, sm->inMotion);
                }
            }
            else {
                transitionSequence.push_back(sm->t_7);
                handle = new __smbase::EventHandle(transitionSequence, sm->inMotion);
            }
            removeWaited(e);
        }
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::InMotion::entry() {
    __smbase::Event *e;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    Engine *context = static_cast<Engine *>(sm->context);

    context->__InMotionEntry();

    e = new __smbase::Event(Engine::__Gravity);
    addWaited(e);
    sm->postTimeEvent(e, context->__T_1When());

    if(this == stateMachine->getInnermostActive()) {
        stateMachine->setInnermostActive(sm->initialInMotion);
    }
}

void Engine::EngineStateMachine::InMotion::exit() {
    clearWaited();
}

Engine::EngineStateMachine::InitialInMotion::InitialInMotion(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::InitialInMotion::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_13);
        handle = new __smbase::EventHandle(transitionSequence, sm->drawing);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::InitialInMotion::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::InitialTop::InitialTop(__smbase::StateMachine *sm) : __smbase::State(sm) { }

__smbase::EventHandle *Engine::EngineStateMachine::InitialTop::handleEvent(__smbase::Event *e) {
    __smbase::EventHandle *handle = 0;
    std::vector<__smbase::Transition *> transitionSequence;
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);

    switch(e->getName()) {
        case __smbase::StateMachine::COMPLETION:

        transitionSequence.push_back(sm->t_3);
        handle = new __smbase::EventHandle(transitionSequence, sm->initialized);
        break;
    }
    return handle;
}

void Engine::EngineStateMachine::InitialTop::doActivity() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    sm->postCompletionEvent(new __smbase::Event(__smbase::StateMachine::COMPLETION));
}

Engine::EngineStateMachine::T_2::T_2(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Engine::EngineStateMachine::T_2::executeEffect() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    static_cast<Engine *>(sm->context)->__T_2Effect();
}

Engine::EngineStateMachine::T_8::T_8(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_9::T_9(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_10::T_10(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_15::T_15(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_16::T_16(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_17::T_17(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_19::T_19(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_22::T_22(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_24::T_24(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Engine::EngineStateMachine::T_24::executeEffect() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    static_cast<Engine *>(sm->context)->__T_24Effect();
}

Engine::EngineStateMachine::T_1::T_1(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_0::T_0(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_3::T_3(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_4::T_4(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_5::T_5(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_6::T_6(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_7::T_7(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Engine::EngineStateMachine::T_7::executeEffect() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    static_cast<Engine *>(sm->context)->__T_7Effect();
}

Engine::EngineStateMachine::T_11::T_11(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

void Engine::EngineStateMachine::T_11::executeEffect() {
    EngineStateMachine *sm = static_cast<EngineStateMachine *>(stateMachine);
    static_cast<Engine *>(sm->context)->__T_11Effect();
}

Engine::EngineStateMachine::T_12::T_12(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_13::T_13(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_14::T_14(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_18::T_18(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_20::T_20(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_21::T_21(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }

Engine::EngineStateMachine::T_23::T_23(bool b, __smbase::StateMachine *sm) : __smbase::Transition(b, sm) { }
