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

# Implementacion de subconjunto del metamodelo del UML 1.4.
# Las clases de elementos son diccionarios. Los atributos y asociaciones
# de estas clases se agregan a traves del metodo set.

from exception import BadElementCompositionError

# Clase base ModelElement.
class ModelElement(dict):

    # Identificador del elemento es obligatorio en toda instancia
    def __init__(self, xmi_id, name=None):

        # Todos los atributos de elementos son tuplas: el primer item
        # es donde guardo el objeto valor, el segundo item
        # es la lista de clases de los cuales puede ser
        # instancia el objeto que guarde
        self['xmi.id'] = (xmi_id, [u''.__class__])
        self['name'] = (name, [u''.__class__])
        self['stereotype'] = ([], [u''.__class__]) # xmi.idref a Stereotype
        self['taggedValue'] = ([], [TaggedValue])

    # Establece el atributo 'attribute' a 'value'
    def set(self, attribute, value):

        valueClass = value.__class__

        # Si trato de dar un valor incorrecto a un atributo
        # se levanta una excepcion
        if valueClass not in self[attribute][1]:
            raise BadElementCompositionError(attribute, self.__class__,
                                             self[attribute][1])

        # Si es un atributo ordenado o una lista de xmi.idref
        if self[attribute][0].__class__ == [].__class__:
            self[attribute][0].append(value)

        # Si es un atributo desordenado
        elif self[attribute][0].__class__ == {}.__class__:

            # Si es el primero de una clase de elementos en el atributo
            if valueClass not in self[attribute][0].keys():
                self[attribute][0][valueClass] = {}

            self[attribute][0][valueClass][value['xmi.id'][0]] = value

        # Si es un otro elemento o un xmi.idref
        else:
            self[attribute] = (value, self[attribute][0])

    # Devuelve el valor de un atributo del elemento
    def get(self, attribute, className=None):

        # Si es un atributo no ordenado y me das el nombre de la clase
        # te devuelvo el diccionario de elementos de esa clase
        if self[attribute][0].__class__ == {}.__class__ and className:

            if className in self[attribute][0].keys():
                return self[attribute][0][className]
            else:
                return {}

        return self[attribute][0]

    # Si el valor del atributo es un string que designa algo
    # devuelvo que es de la clase string.
    # Si puede ser una instancia devuelve None
    def getAttributeCharacter(self, attribute):

        if u''.__class__ in self[attribute][1]:
            return u''.__class__

        return None

# Elemento abstracto Namespace
class Namespace(ModelElement):

    # Clases de elementos validos para atributo 'ownedElement'
    validOwnedElements = []

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

        self['ownedElement'] = ({}, self.validOwnedElements)


class Package(Namespace):

    def __init__(self, xmi_id, name):

        self.validOwnedElements = [Model, Package, Class, Interface,
                                   Generalization, Association, Dependency,
                                   Abstraction]

        Namespace.__init__(self, xmi_id, name)


class Model(Namespace):

    def __init__(self, xmi_id, name):

        self.validOwnedElements = [DataType, Stereotype, TagDefinition,
                                   Class, Interface, Generalization,
                                   Association, Dependency, Abstraction,
                                   Model, Package, CallEvent,
                                   TimeEvent]

        Namespace.__init__(self, xmi_id, name)


class Stereotype(ModelElement):

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

        self['baseClass'] = (None, [u''.__class__])


class TagDefinition(ModelElement):

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

        self['tagType'] = (None, [u''.__class__])
        self['multiplicity'] = (None, [Multiplicity])


class TaggedValue(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['dataValue'] = (None, [u''.__class__])
        self['type'] = (None, [u''.__class__]) # xmi.idref a TagDefinition


class DataType(ModelElement):

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

# Elemento abstracto Classifier
class Classifier(ModelElement):

    # Clases de elementos validos para atributo 'feature'
    validFeatures = []

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

        self['visibility'] = (None, [u''.__class__])
        self['isLeaf'] = (None, [u''.__class__])
        self['isAbstract'] = (None, [u''.__class__])
        self['feature'] = ({}, self.validFeatures)
        self['clientDependency'] = ([], [u''.__class__])
        self['generalization'] = ([], [u''.__class__])


class Class(Classifier, Namespace):

    def __init__(self, xmi_id, name):

        self.validOwnedElements = [Class, Interface, StateMachine,
                                   ActivityGraph]
        self.validFeatures = [Attribute, Operation, Method]

        Classifier.__init__(self, xmi_id, name)
        Namespace.__init__(self, xmi_id, name)


class Feature(ModelElement):

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

        self['visibility'] = (None, [u''.__class__])
        self['ownerScope'] = (None, [u''.__class__])


class Attribute(Feature):

    def __init__(self, xmi_id, name):

        Feature.__init__(self, xmi_id, name)

        # xmi.idref DataType | Class | Interface
        self['type'] = (None, [u''.__class__])
        # changeable | frozen | addOnly
        self['changeability'] = (None, [u''.__class__])
        self['initialValue'] = (None, [Expression])
        self['multiplicity'] = (None, [Multiplicity])


class Multiplicity(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['range'] = (None, [MultiplicityRange])


class MultiplicityRange(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['lower'] = (None, [u''.__class__])
        self['upper'] = (None, [u''.__class__])


class Operation(Feature):

    def __init__(self, xmi_id, name):

        Feature.__init__(self, xmi_id, name)

        self['isAbstract'] = (None, [u''.__class__])
        self['isQuery'] = (None, [u''.__class__])
        self['isLeaf'] = (None, [u''.__class__])
        self['parameter'] = ([], [Parameter])


class Parameter(ModelElement):

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

        # in | out | inout | return
        self['kind'] = (None, [u''.__class__])
        # xmi.dref DataType | Class | Interface
        self['type'] = (None, [u''.__class__])
        self['defaultValue'] = (None, [Expression])


class Method(Feature):

    def __init__(self, xmi_id, name=None):

        Feature.__init__(self, xmi_id, name)

        self['body'] = (None, [ProcedureExpression])
        self['specification'] = (None, [u''.__class__])


class Expression(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['body'] = (None, [u''.__class__])
        self['language'] = (None, [u''.__class__])


class ProcedureExpression(Expression):

    pass


class Interface(Classifier, Namespace):

    def __init__(self, xmi_id, name):

        self.validFeatures = [Operation]
        self.validOwnedElements = [Class, Interface]

        Classifier.__init__(self, xmi_id, name)
        Namespace.__init__(self, xmi_id, name)
        
class Generalization(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        # Nota: child y parent deben ser identificadores de
        # referencia al mismo tipo de elemento
        self['child'] = (None, [u''.__class__])  #xmi.idref Classifier
        self['parent'] = (None, [u''.__class__]) #xmi.idref Classifier

# Asociacion del UML
class Association(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['connection'] = ({}, [AssociationEnd])


class AssociationEnd(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['multiplicity'] = (None, [Multiplicity])
        # xmi.idref Class | Interface
        self['participant'] = (None, [u''.__class__])
        self['visibility'] = (None, [u''.__class__])
        self['changeability'] = (None, [u''.__class__])
        self['isNavigable'] = (None, [u''.__class__])   # true | false
        self['targetScope'] = (None, [u''.__class__])   # classifier | instance
        # composite | agregate | none
        self['aggregation'] = (None, [u''.__class__])


class Dependency(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['client'] = (None, [u''.__class__])    # xmi.idref Class | Interface
        self['supplier'] = (None, [u''.__class__])  # xmi.idref Class | Interface

# Abstraccion del UML. Este elemento esta aca, pues con el estereotipo
# <<realize>> se convierte en una realizacion de interfaz.
class Abstraction(Dependency):

    pass


class CallEvent(ModelElement):

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

        # Nota: que son estos, parametros formales o actuales ?
        # Segun la especificacion del UML son parametros formales
        # no es necesario
        self['operation'] = (None, [u''.__class__])  # xmi.idref Operation


class TimeEvent(ModelElement):

    def __init__(self, xmi_id, name):

        ModelElement.__init__(self, xmi_id, name)

        self['when'] = (None, [TimeExpression])


class TimeExpression(Expression):

    pass

#Maquina de estados del UML
class StateMachine(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['context'] = (None, [u''.__class__])  # xmi.idref a Class
        self['top'] = (None, [CompositeState])
        self['transition'] = ({}, [Transition])


class StateVertex(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['incoming'] = ([], [u''.__class__])  # xmi.idref a Transition
        self['outgoing'] = ([], [u''.__class__])  # xmi.idref a Transition


class Pseudostate(StateVertex):

    def __init__(self, xmi_id, name=None):

        StateVertex.__init__(self, xmi_id, name)

        self['kind'] = (None, [u''.__class__])


class State(StateVertex):

    def __init__(self, xmi_id, name=None):

        StateVertex.__init__(self, xmi_id, name)

        actions = [ActionSequence, UninterpretedAction, ReturnAction]

        self['entry'] = (None, actions)
        self['doActivity'] = (None, actions)
        self['exit'] = (None, actions)


class CompositeState(State):

    def __init__(self, xmi_id, name=None):

        self.validSubvertex = [CompositeState, SimpleState, FinalState,
                               Pseudostate, ActionState]

        State.__init__(self, xmi_id, name)

        self['subvertex'] = ({}, self.validSubvertex)


class SimpleState(State):

    def __init__(self, xmi_id, name):

        # Con esto obligo a que estos estados tengan nombre
        State.__init__(self, xmi_id, name)


class FinalState(State):

    pass

# Transicion del UML
class Transition(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        # xmi.idref a Pseudostate o SimpleState
        self['source'] = (None, [u''.__class__])
        # xmi.idref a SimpleState, FinalState o Pseudostate
        self['target'] = (None, [u''.__class__])
        # xmi.idref a CallEvent o TimeEvent
        self['trigger'] = (None, [u''.__class__])
        self['effect'] = (None, [ActionSequence, UninterpretedAction])
        self['guard'] = (None, [Guard])


class Guard(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['expression'] = (None, [BooleanExpression])

# Expresion booleana
class BooleanExpression(Expression):

    pass

# Accion
class Action(ModelElement):

    def __init__(self, xmi_id, name=None):

        ModelElement.__init__(self, xmi_id, name)

        self['script'] = (None, [ActionExpression])

# Secuencia de acciones
# La secuencia de acciones es tambien una accion, mas
# no me interesa tener una sola expresion asociada a esta
class ActionSequence(Action):

    def __init__(self, xmi_id, name=None):

        Action.__init__(self, xmi_id, name)

        self['action'] = ([], [ActionSequence, UninterpretedAction,
                               ReturnAction])

# Accion generica. Esta representa una sentencia en algun lenguaje
class UninterpretedAction(Action):

    pass

# Accion de devolucion.
class ReturnAction(Action):

    pass

# Expresion de accion
class ActionExpression(Expression):

    pass

# Grafo de actividades
class ActivityGraph(StateMachine):

    pass

# Estado de accion
class ActionState(SimpleState):

    pass
