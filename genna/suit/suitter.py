##======================================================================
##
## Copyright (C) 2007. Mario Rincon Nigro.
## Universidad de Los Andes.
##
## This file is part of Genna.
##
## Genna is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 2 of the License, or
## (at your option) any later version.
##
## Genna is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Genna.  If not, see <http://www.gnu.org/licenses/>.
##
##======================================================================

# Este modulo tiene como fin crear una representacion
# mas apropiada de los objetos del modulo uml.element,
# para la generacion de codigo.
# Ordena atributos y metodos segun visibilidad, etc.
# Resuelve los nombres de referencias

import settings
import exception

from uml.element import *
from suit.aide import fullNames, fullAssociations, fullOwnDependencies

# Tabla de elementos
_table = {}
# Tabla de nombres en jerarquia de nombres
_namespaces = {}
# Tabla de dependencias de classifier
_dependencies = {}
# Tabla de asociaciones para classifier
_associations = {}


def _elementQuerier(element, query):

    actualElement = element

    if not issubclass(actualElement.__class__, ModelElement):
        raise exception.NotAModelElement

    for item in query:

        if actualElement == None:
            raise exception.NotAModelElement

        foundStuff = actualElement.get(item)

        if foundStuff == None:
            break

        if foundStuff.__class__ != u''.__class__:
            actualElement = foundStuff
        elif foundStuff in _table.keys():
            actualElement = _table[foundStuff]
        else:   # Cuidado con esto, es para forzar errores logicos
            actualElement = None

    return foundStuff


# Representa el modelo usado por las plantillas de generacion
# de codigo, acomodado de la tabla de elementos de modelo
class RootModelSuitter:

    def __init__(self, table):

        global _table
        global _namespaces
        global _dependencies
        global _associations

        _table = table
        _namespaces = fullNames(table)
        _associations = fullAssociations(table)
        _dependencies = fullOwnDependencies(table, _namespaces, _associations)

        self.suittedModel = SuittedModel(table.root_key)

    def getRootModel(self):

        return self.suittedModel


class SuittedElement(dict):

    # Recibe el xmi.id del elemento a acomodar y la tabla de todos
    # los elementos del modelo
    def __init__(self, xmi_id):

        self.umlElement = _table[xmi_id]

        self['name'] = self.suitString(['name'])
        # idref [], valor
        self['stereotype'] = self.suitStringList(['stereotype'], ['name'])
        self['taggedValues'] = self.suitTaggedValues()

    def suitString(self, query):

        suittedString = _elementQuerier(self.umlElement, query)

        if suittedString.__class__ != u''.__class__:
            if suittedString == None:
                return ''
            raise exception.NotAStringError

        return suittedString

    def suitBoolean(self, query):

        return self.suitString(query) == 'true'

    def suitStringList(self, listQuery, elementQuery):

        suittedList = []
        initialList = _elementQuerier(self.umlElement, listQuery)

        if initialList.__class__ != [].__class__:
            raise exception.NotASequenceError

        for _id in initialList:
            actualElement = _table[_id]
            newElement = _elementQuerier(actualElement, elementQuery)

            if newElement.__class__ != u''.__class__:
                # print actualElement
                # print newElement
                raise exception.NotAStringError
            suittedList.append(newElement)

        return suittedList

    def suitTaggedValues(self):

        suittedTags = []

        for tag in self.umlElement.get('taggedValue'):
            suittedTags.append(SuittedTaggedValue(tag.get('xmi.id')))

        return suittedTags


class SuittedTaggedValue(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        self['dataValue'] = self.suitString(['dataValue'])
        self['type'] = self.suitString(['type', 'name']) #id_ref, valor


class SuittedNamespace(SuittedElement):

    def __init__(self, xmi_id):

       SuittedElement.__init__(self, xmi_id)

    # Acomoda elementos pertenecientes al namespace,
    # suittedClassName es la clase acomodada y umlClassName
    # la clase del elemento a acomodar
    def suitOwnedElements(self, suittedClassName, umlClassName):

        suitted = []
        # Se agregan los elementos
        for _id in self.umlElement.get('ownedElement', umlClassName).keys():
            suitted.append(suittedClassName(_id))

        return suitted


class SuittedPackage(SuittedNamespace):

    def __init__(self, xmi_id):

        SuittedNamespace.__init__(self, xmi_id)

        self['namespace'] = _namespaces[xmi_id]
        self['package'] = self.suitOwnedElements(SuittedPackage, Package)
        self['model'] = self.suitOwnedElements(SuittedModel, Model)
        self['class'] = self.suitOwnedElements(SuittedClass, Class)
        self['interface'] = self.suitOwnedElements(SuittedInterface, Interface)
        self['hasStateMachine'] = self.suitHasStateMachine()

    def suitHasStateMachine(self):

        for package in self['package'] + self['model']:
            if package['hasStateMachine']:
                return True

        for _class in self['class']:
            if _class['hasStateMachine']:
                return True

        return False


class SuittedModel(SuittedPackage):

    pass


class SuittedClassifier(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

    def suitFeatures(self, suittedClassName, umlClassName, ftrd_xmi_id, ftrdStateMachines=[]):

        suittedStuff = {'public': [], 'package': [],
                        'protected': [], 'private': []}

        argsMap = {Attribute: (), Operation: (ftrd_xmi_id, ftrdStateMachines)}

        # Se agregan los atributos
        for _id in self.umlElement.get('feature', umlClassName).keys():
            args = (_id, ) + argsMap[umlClassName]
            visibility = _table[_id].get('visibility')
            suittedStuff[visibility].append(apply(suittedClassName, args))

        # Se agregan las asociaciones como atributos si
        if umlClassName == Attribute:
            # Se agregan como atributos todos los extremos opuestos
            # navegables de las asociaciones de esta clase.
            for _id in _associations[ftrd_xmi_id]:
                if _table[_id].get('isNavigable') == 'true':
                    visibility = _table[_id].get('visibility')
                    suittedStuff[visibility].append(SuittedAssociationEnd(_id))

        return suittedStuff


class SuittedClass(SuittedClassifier, SuittedNamespace):

    def __init__(self, xmi_id):

        SuittedClassifier.__init__(self, xmi_id)

        self['namespace'] = _namespaces[xmi_id]
        self['visibility'] = self.suitString(['visibility'])
        self['isLeaf'] = self.suitBoolean(['isLeaf'])
        self['isAbstract'] = self.suitBoolean(['isAbstract'])
        self['generalize'] = self.suitStringList(['generalization'], ['parent', 'name'])

        if settings.BEHAVIORAL_GENERATION == settings.STATE_MACHINES or \
           settings.BEHAVIORAL_GENERATION == settings.FULL:
            self['stateMachine'] = self.suitOwnedElements(SuittedStateMachine, StateMachine)
        else:
            self['stateMachine'] = []
            
        self['attribute'] = self.suitFeatures(SuittedAttribute, Attribute, xmi_id)
        self['operation'] = self.suitFeatures(SuittedOperation, Operation, xmi_id,
                                              self['stateMachine'])
        self['classes'] = self.suitOwnedElements(SuittedClass, Class)
        self['dependency'] = self.suitDependencies()
        self['realize'] = self.suitRealizations()
        self['hasStateMachine'] = self.suitHasStateMachine()

    def suitRealizations(self):

        realizations = []

        # Se agregan las interfaces que realiza
        for _id in self.umlElement.get('clientDependency'):

            # Esto lo hago solo porque necesito conocer los estereotipos
            # de la abstraccion
            abstraction = SuittedElement(_id)

            if 'realize' in abstraction['stereotype']:
                supplier = _table[_id].get('supplier')
                realizations.append(_table[supplier].get('name'))

        return realizations

    def suitDependencies(self):
        # Se agregan las dependencias propias
        dependencies = _dependencies[self.umlElement.get('xmi.id')]

        # Se agregan las dependencias que inducen las clases internas
        for innerClass in self['classes']:
            dependencies += innerClass['dependency']

        dependencies.sort()

        return dependencies

    def suitHasStateMachine(self):

        if self['stateMachine']:
            return True

        for _class in self['classes']:
            if _class['hasStateMachine']:
                return True

        return False

class SuittedInterface(SuittedClassifier):

    def __init__(self, xmi_id):

        SuittedClassifier.__init__(self, xmi_id)

        self['namespace'] = _namespaces[xmi_id]
        self['dependency'] = _dependencies[xmi_id]
        self['visibility'] = self.suitString(['visibility'])
        self['isLeaf'] = self.suitBoolean(['isLeaf'])
        self['operation'] = self.suitFeatures(SuittedOperation, Operation, xmi_id)
        #idref [], idref, valor
        self['generalize'] = self.suitStringList(['generalization'], ['parent', 'name'])


class SuittedAttribute(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        self['ownerScope'] = self.suitString(['ownerScope'])
        self['visibility'] = self.suitString(['visibility'])
        self['type'] = self.suitString(['type', 'name'])   #idref, valor
        self['changeability'] = self.suitString(['changeability'])
        # ref, valor
        self['initialValue'] = self.suitString(['initialValue', 'body'])
        # ref, ref, valor
        self['multiplicity'] = self.suitString(['multiplicity', 'range', 'upper'])
        self['isAssociation'] = False

    def __cmp__(self, y):

        # Se comparan los ambitos
        if self['ownerScope'] < y['ownerScope']:
            return -1
        if self['ownerScope'] > y['ownerScope']:
            return 1

        # Se comparan los tipos
        if self['type'] < y['type']:
            return -1
        if self['type'] > y['type']:
            return 1

        # Se comparan los nombres
        if self['name'] < y['name']:
            return -1
        if self['name'] > y['name']:
            return 1

        return 0


class SuittedAssociationEnd(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        self['ownerScope'] = self.suitString(['targetScope'])
        self['visibility'] = self.suitString(['visibility'])
        self['type'] = self.suitString(['participant', 'name']) #idref, valor
        self['changeability'] = self.suitString(['changeability'])
        self['initialValue'] = ''
        #ref, ref, valor
        self['multiplicity'] = self.suitString(['multiplicity', 'range', 'upper'])
        self['isAssociation'] = True


class SuittedOperation(SuittedElement):

    def __init__(self, xmi_id, ftrd_xmi_id, ftrdStateMachines):

        SuittedElement.__init__(self, xmi_id)

        self['visibility'] = self.suitString(['visibility'])
        self['ownerScope'] = self.suitString(['ownerScope'])
        self['isLeaf'] = self.suitBoolean(['isLeaf'])
        self['isAbstract'] = self.suitBoolean(['isAbstract'])
        self['isQuery'] = self.suitBoolean(['isQuery'])
        self['parameter'] = self.suitParameters()
        self['method'] = self.suitMethod(ftrd_xmi_id)
        self['callEvent'] = self.suitRelatedCallEvent(ftrdStateMachines)
        self['return'] = self.suitReturned()

        if settings.BEHAVIORAL_GENERATION == settings.ACTIVITY_GRAPHS or \
           settings.BEHAVIORAL_GENERATION == settings.FULL:
            self['activityGraph'] = self.suitActivityGraph(ftrd_xmi_id)
        else:
            self['activityGraph'] = None

    def suitParameters(self):

        parameters = []

        for parameter in self.umlElement.get('parameter'):
            _id = parameter.get('xmi.id')

            if parameter.get('kind') != 'return':
                parameters.append(SuittedParameter(_id))

        return parameters

    def suitMethod(self, ftrd_xmi_id):

        suitted = ''

        # Se agrega a la operacion el metodo que la implemente
        for method in _table[ftrd_xmi_id].get('feature', Method).values():
            if method.get('specification') == self.umlElement.get('xmi.id'):
                suitted = _elementQuerier(method, ['body', 'body'])
                break

        return suitted

    def suitReturned(self):

        returned = None

        for parameter in self.umlElement.get('parameter'):
            if parameter.get('kind') == 'return':
                _id = parameter.get('xmi.id')
                returned = SuittedParameter(_id)
                break

        return returned

    def suitRelatedCallEvent(self, ftrdStateMachines):

        relatedCallEvents = []

        # Se agregan a la operacion las transiciones con eventos
        # CallEvent que se refieren a ella
        callTransitions = []

        for machine in ftrdStateMachines:
            callTransitions.extend(machine['transition']['callEvent'])

        for transition in callTransitions:
            if transition['trigger']['operation'] == self.umlElement.get('xmi.id'):
                if transition['trigger'] not in relatedCallEvents:
                    relatedCallEvents.append(transition['trigger'])

        return relatedCallEvents

    def suitActivityGraph(self, ftrd_xmi_id):

        suittedActivityGraph = None
        activityGraphs = _table[ftrd_xmi_id].get('ownedElement', ActivityGraph).keys()

        for _id in activityGraphs:

            if _table[_id].get('context') == self.umlElement.get('xmi.id'):
                suittedActivityGraph = SuittedActivityGraph(_id)
                break

        return suittedActivityGraph


class SuittedParameter(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        self['type'] = self.suitString(['type', 'name']) #idref, valor
        self['kind'] = self.suitString(['kind'])
        self['defaultValue'] = self.suitString(['defaultValue', 'body']) # ref, valor

# Maquina de estados
class SuittedStateMachine(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        # xmi.id del estado tope de la maquina
        top_xmi_id = self.umlElement.get('top').get('xmi.id')

        # Los siguientes diccionarios son auxiliares para resolver
        # referencias. Las claves son xmi.idref y los valores
        # son objetos SuittedTransition y SuittedState, respectivamente.
        stateMap = self.makeStateMap(top_xmi_id, None)
        transitionMap = self.makeTransitionMap()

        self['top'] = stateMap[top_xmi_id]
        self['context'] = self.suitString(['context']) # xmi.idref
        self['states'] = self.suitStates(stateMap, transitionMap)
        self['transition'] = self.suitTransitions(stateMap, transitionMap)

    # Se crea un diccionario con todos los estados de la maquina de estados.
    def makeStateMap(self, xmi_id, ancestor_xmi_id):

        stateMap = {}
        stateClasses = [SimpleState, CompositeState, Pseudostate,
                        FinalState, ActionState]

        stateMap[xmi_id] = SuittedCompositeState(xmi_id, ancestor_xmi_id)

        for name in stateClasses:
            for _id in _table[xmi_id].get('subvertex', name).keys():
                state = _table[_id]

                if state.__class__ == CompositeState:
                    stateMap.update(self.makeStateMap(_id, xmi_id))

                elif state.__class__ == SimpleState:
                    stateMap[_id] = SuittedSimpleState(_id, xmi_id)

                elif state.__class__ == Pseudostate:
                    stateMap[_id] = SuittedPseudostate(_id, xmi_id)

                elif state.__class__ == FinalState:
                    stateMap[_id] = SuittedFinalState(_id, xmi_id)

                elif state.__class__ == ActionState:
                    stateMap[_id] = SuittedActionState(_id, xmi_id)

        return stateMap

    # Se crea un diccionario con todas las transiciones de la maquina
    # de estados. 
    def makeTransitionMap(self):

        transitionMap = {}

        i = 0;

        for _id in self.umlElement.get('transition', Transition).keys():
            transitionMap[_id] = SuittedTransition(_id)
            transitionMap[_id]['name'] = 'T_' + str(i)
            i += 1

        return transitionMap

    def suitStates(self, stateMap, transitionMap):

        suittedStates = {'simpleState': [], 'pseudostate': [],
                         'compositeState': [], 'actionState': [],
                         'finalState':[]}

        # Para cada estado en la maquina de estado
        for _id in stateMap.keys():

            state = stateMap[_id]

            # Para cada transicion entrante y saliente del estado
            for direction in ['incoming', 'outgoing']:
                # Paa cada trigger que pueda tener la transicion
                for trigger in state[direction].keys():

                    new_transitions = []

                    # Se agrega una referencia a la transicion a una lista
                    for transition_id in state[direction][trigger]:

                        transition = transitionMap[transition_id]
                        new_transitions.append(transition)

                    # Se ordenana la lista de transiciones
                    # y se agrega al estado clasificando
                    # segun direccion y tipo de trigger
                    new_transitions.sort()
                    state[direction][trigger] = new_transitions

            maps = {SimpleState: 'simpleState', CompositeState: 'compositeState',
                    Pseudostate: 'pseudostate', ActionState: 'actionState',
                    FinalState: 'finalState'}

            stateClass = _table[_id].__class__

            # Se resuelve la referencia al ancestro directo
            if state['directAncestor']:
                state['directAncestor'] = stateMap[state['directAncestor']]

            # Si el estado es compuesto, se resuelve la referencia a su estado
            # inicial
            if stateClass == CompositeState:
                if state['initial']:
                    state['initial'] = stateMap[state['initial']]

            # Se agrega el estado al diccionario de estados clasificando de
            # acuerdo a su tipo
            if stateClass in maps.keys():
                suittedStates[maps[stateClass]].append(state)

        return suittedStates

    def suitTransitions(self, stateMap, transitionMap):

        suittedTransitions = {'callEvent': [], 'timeEvent': [], 'none': []}

        # Se agregan todas las transiciones y se resuelven los xmi.idref
        # de sus estados fuente y destino
        for _id in transitionMap.keys():

            transition = transitionMap[_id]

            source_id = transition['source']
            target_id = transition['target']
            transition['source'] = stateMap[source_id]
            transition['target'] = stateMap[target_id]

            trigger_id = _table[_id].get('trigger')

            if not trigger_id:
                suittedTransitions['none'].append(transition)
            elif _table[trigger_id].__class__ == CallEvent:
                suittedTransitions['callEvent'].append(transition)
            elif _table[trigger_id].__class__ == TimeEvent:
                suittedTransitions['timeEvent'].append(transition)

        return suittedTransitions

# Clase base para estados de maquina de estados
class SuittedState(SuittedElement):

    def __init__(self, xmi_id, ancestor_xmi_id):

        SuittedElement.__init__(self, xmi_id)

        self['entry'] = self.suitActivity('entry')
        self['doActivity'] = self.suitActivity('doActivity')
        self['exit'] = self.suitActivity('exit')
        self['outgoing'] = self.suitOutgoingTransitions()
        # 
        self['incoming'] = {} #self.suitTransitions('incoming')
        # xmi.idref a estado ancestro directo
        self['directAncestor'] = ancestor_xmi_id
        # Cadena que indica que tipo de estado es:
        # simpleState, compositeState, finalState, pseudostate,
        # actionState
        self['type'] = self.suitType()
        self['hasOutgoingTimeEvent'] = self.suitHasOutgoingTimeEvent()

    def suitActivity(self, activityKind):

        # Se agregan las actividades al estado
        if self.umlElement.__class__ != Pseudostate:

            activity = self.umlElement.get(activityKind)

            if activity:
                _id = activity.get('xmi.id')
                return SuittedAction(_id)['expression']

        return []

    def suitOutgoingTransitions(self):

        suittedTransitions = {}

        # Transicion de estado inicial. Esto se debe a que la transicion
        # del estado inicial para un grafo de actividades puede estar
        # asociada a un callEvent
        if self.umlElement.__class__ == Pseudostate and \
               self.umlElement.get('kind') == 'initial':
            for _id in self.umlElement.get('outgoing'):
                suittedTransitions['none'] = [_id]

        else:
            # Se agregan las transiciones al estado
            # Estos xmi.idref se resuelven en SuittedStateMachine
            for _id in self.umlElement.get('outgoing'):
                trigger_id = _table[_id].get('trigger')

                if not trigger_id:
                    trigger_key = 'none'
                else:
                    trigger_key = _table[trigger_id].get('name')

                if trigger_key not in suittedTransitions:
                    suittedTransitions[trigger_key] = []

                suittedTransitions[trigger_key].append(_id)

        return suittedTransitions

    def suitType(self):

        maps = {SimpleState: 'simpleState', CompositeState: 'compositeState',
                Pseudostate: 'pseudostate', FinalState: 'finalState',
                ActionState: 'actionState'}

        return maps[self.umlElement.__class__]

    def suitHasOutgoingTimeEvent(self):

        for _id in self.umlElement.get('outgoing'):
            transition = _table[_id]
            trigger_id = transition.get('trigger')

            if trigger_id:
                if _table[trigger_id].__class__ == TimeEvent:
                    return True

        return False

class SuittedCompositeState(SuittedState):

    def __init__(self, xmi_id, ancestor_xmi_id):

        SuittedState.__init__(self, xmi_id, ancestor_xmi_id)

        # xmi.idref a estado inicial
        self['initial'] = self.suitInitial()
        # lista de xmi.idref de subestados
        # Esto lo estoy usando para algo?
        self['subvertex'] = self.suitSubvertexes();

    def suitInitial(self):

        # Se busca el estado inicial
        for _id in self.umlElement.get('subvertex', Pseudostate).keys():

            if _table[_id].get('kind') == 'initial':
                return _id

    def suitSubvertexes(self):

        subvertexes = {'simpleState': [], 'compositeState': [], 'pseudostate': [],
                       'finalState': [], 'actionState': []}

        nameClass = {'simpleState': SimpleState, 'compositeState': CompositeState,
                     'pseudostate': Pseudostate, 'finalState': FinalState,
                     'actionState': ActionState}

        for key in nameClass.keys():
            subvertexes[key] = self.umlElement.get('subvertex', nameClass[key]).keys()

        return subvertexes


class SuittedSimpleState(SuittedState):

    pass


class SuittedPseudostate(SuittedState):

    def __init__(self, xmi_id, ancestor_xmi_id):

        SuittedState.__init__(self, xmi_id, ancestor_xmi_id)

        self['kind'] = self.suitString(['kind'])

class SuittedActionState(SuittedState):

    pass


class SuittedFinalState(SuittedState):

    pass

# Transicion de estados
class SuittedTransition(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        # Nota: los xmi.idref source y target se resuelven en SuittedStateMachine
        # Nota: trigger puede ser un xmi.idref si es un CallEvent, este
        # se resuelve en SuittedOperation

        # Cadena con expresion guardia
        self['guard'] = self.suitString(['guard', 'expression', 'body']) #ref, ref, valor
        # Lista de cadenas con expresiones de efectos 
        self['effect'] = self.suitEffect()
        # Referencia a evento trigger
        self['trigger'] = self.suitTrigger()
        # xmi.idref a estado fuente
        self['source'] = self.suitString(['source']) # xmi.idref
        #xmi.idref a estado objetivo
        self['target'] = self.suitString(['target']) # xmi.idref

    def __cmp__(self, y):

        elses = ['', 'else']

        # self < y
        if (self['guard'] not in elses) and (y['guard'] in elses):
            return -1

        if (self['guard'] not in elses) == (y['guard'] not in elses):
            return 0

        if (self['guard'] in elses) and (y['guard'] not in elses):
            return 1

    def suitTrigger(self):

        # Se agrega el evento
        _id = self.umlElement.get('trigger')

        if _id:
            trigger = _table[_id]

            if trigger.__class__ == CallEvent:
                return SuittedCallEvent(_id)

            elif trigger.__class__ == TimeEvent:
                return SuittedTimeEvent(_id)

        return None

    def suitEffect(self):

        effect = self.umlElement.get('effect')

        if effect:
            return SuittedAction(effect.get('xmi.id'))['expression']

        return []

# Evento de tiempo. when es una expresion que indica cuando
# debe dispararse este evento.
class SuittedTimeEvent(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        # Cadena con expresion que indica un tiempo relativo
        self['when'] = self.suitString(['when', 'body']) # ref, value

# Evento de llamada a operacion. operation es el xmi.id
# de la operacion asociada. Este xmi.id es resuelto en SuittedOperation
class SuittedCallEvent(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        # xmi.idref de operacion asociada
        self['operation'] = self.suitString(['operation']) #xmi.id

# Accion. Secuencia de expresiones.
class SuittedAction(SuittedElement):

    def __init__(self, xmi_id):

        SuittedElement.__init__(self, xmi_id)

        # Lista de cadenas. Cada cadena es una expresion
        self['expression'] = self.suitExpression()

    def suitExpression(self):

        expression = []

        if self.umlElement.__class__ in [UninterpretedAction, ReturnAction]:
            expression.append(self.suitString(['script', 'body']))

        elif self.umlElement.__class__ == ActionSequence:

            for action in self.umlElement.get('action'):
                activity = SuittedAction(action.get('xmi.id'))
                expression.extend(activity['expression'])

        return expression

# Grafo de actividad. Cada estado es etiquetado con un valor
# unico para la generacion de codigo.
class SuittedActivityGraph(SuittedStateMachine):

    def __init__(self, xmi_id):

        SuittedStateMachine.__init__(self, xmi_id)
        label = 0

        for name in ['pseudostate', 'actionState', 'finalState']:
            for state in self['states'][name]:
                state['label'] = label
                label += 1
