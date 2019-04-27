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

# Este modulo contiene clases para extraer elementos
# del contenido de un documento XMI.
# Estas funciones son auxiliares al modulo
# xmi.handler

import string

from xml.dom.ext.reader.Sax2 import FromXmlStream
from xml.xpath import Compile
from xml.xpath.Context import Context

from uml.element import *


# Evalua consulta XPath, en contexto content
def evaluateXPath(content, xpath):

    # Variables necesarias para establecer el espacio de nombres de un
    # contexto para consultas XPath
    UML_PREFIX = 'UML'
    UML_URL = 'org.omg.xmi.namespace.UML'

    # Establezco el contenido como contexto para las consultas XPath
    context = Context(content)
    context.setNamespaces({UML_PREFIX: UML_URL})

    # Creo la consulta XPath
    expresion = Compile(xpath)

    # Devuelve evaluacion de la consulta XPath
    return expresion.evaluate(context)

# Devuelve True si el elemento es un elemento reconocido por el generador
# de codigo, False en caso contrario
def isRecognizedElement(xmiElementName):

    return xmiElementName in ExtractorFactory.mapping.keys()


class ExtractorFactory:

    mapping = {
        'UML:Package': 'PackageExtractor',
        'UML:Model': 'ModelExtractor',
        'UML:Stereotype': 'StereotypeExtractor',
        'UML:TagDefinition': 'TagDefinitionExtractor',
        'UML:TaggedValue': 'TaggedValueExtractor',
        'UML:DataType': 'DataTypeExtractor',
        'UML:Class': 'ClassExtractor',
        'UML:Feature': 'FeatureExtractor',
        'UML:Attribute': 'AttributeExtractor',
        'UML:Multiplicity': 'MultiplicityExtractor',
        'UML:MultiplicityRange': 'MultiplicityRangeExtractor',
        'UML:Operation': 'OperationExtractor',
        'UML:Parameter': 'ParameterExtractor',
        'UML:Method': 'MethodExtractor',
        'UML:Expression': 'ExpressionExtractor',
        'UML:ProcedureExpression': 'ProcedureExpressionExtractor',
        'UML:Interface': 'InterfaceExtractor',
        'UML:Generalization': 'GeneralizationExtractor',
        'UML:Association': 'AssociationExtractor',
        'UML:AssociationEnd': 'AssociationEndExtractor',
        'UML:Dependency': 'DependencyExtractor',
        'UML:Abstraction': 'AbstractionExtractor',
        'UML:CallEvent': 'CallEventExtractor',
        'UML:TimeEvent': 'TimeEventExtractor',
        'UML:TimeExpression': 'TimeExpressionExtractor',
        'UML:StateMachine': 'StateMachineExtractor',
        'UML:StateVertex': 'StateVertexExtractor',
        'UML:CompositeState': 'CompositeStateExtractor',
        'UML:Pseudostate': 'PseudostateExtractor',
        'UML:SimpleState': 'SimpleStateExtractor',
        'UML:FinalState': 'FinalStateExtractor',
        'UML:Transition': 'TransitionExtractor',
        'UML:Guard': 'GuardExtractor',
        'UML:BooleanExpression': 'BooleanExpressionExtractor',
        'UML:Action': 'ActionExtractor',
        'UML:ActionSequence': 'ActionSequenceExtractor',
        'UML:UninterpretedAction': 'UninterpretedActionExtractor',
        'UML:ReturnAction': 'ReturnActionExtractor',
        'UML:ActionExpression': 'ActionExpressionExtractor',
        'UML:ActivityGraph': 'ActivityGraphExtractor',
        'UML:ActionState': 'ActionStateExtractor'
        }

    def __init__(self, nodeName):

        self.instance = eval(self.mapping[nodeName])()

    def getExtractorInstance(self):

        return self.instance


class ModelElementExtractor(dict):

    extractClass = None

    def __init__(self):

        self['xmi.id'] = '@xmi.id'
        self['name'] = '@name'
        self['stereotype'] = 'UML:ModelElement.stereotype/' + \
                             'UML:Stereotype/@xmi.idref'
        self['taggedValue'] = 'UML:ModelElement.taggedValue/' + \
                              'UML:TaggedValue'

    # Esto es para depurar unicamente
    def checkAllAttributes(self):

        if self.extractClass:
            instance = self.extractClass('3', '1')

            for key in self.keys():
                if key not in instance.keys():
                    print key + ' en Extractor pero no en Element'

            for key in instance.keys():
                if key not in self.keys():
                    print key + ' en Element pero no en Extractor'


class NamespaceExtractor(ModelElementExtractor):

    elementNames = []

    def __init__(self):

        ModelElementExtractor.__init__(self)

        items = []
        for name in self.elementNames:
            items.append('UML:Namespace.ownedElement/' + name)

        self['ownedElement'] = string.join(items, '|') 


class PackageExtractor(NamespaceExtractor):

    elementNames = ['UML:Model', 'UML:Package', 'UML:Class',
                    'UML:Interface', 'UML:Generalization', 'UML:Association',
                    'UML:Dependency', 'UML:Abstraction']
    extractClass = Package


class ModelExtractor(NamespaceExtractor):

    elementNames = ['UML:DataType', 'UML:Stereotype', 'UML:Class',
                    'UML:Interface', 'UML:Generalization', 'UML:Association',
                    'UML:Dependency', 'UML:Abstraction', 'UML:Model',
                    'UML:Package', 'UML:CallEvent', 'UML:TimeEvent',
                    'UML:TagDefinition', 'UML:Model']
    extractClass = Model


class StereotypeExtractor(ModelElementExtractor):

    extractClass = Stereotype

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['baseClass'] = 'UML:stereotype.baseClass/node()'


class TagDefinitionExtractor(ModelElementExtractor):

    extractClass = TagDefinition

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['tagType'] = 'tagType'
        self['multiplicity'] = 'UML:TagDefinition.multiplicity/' + \
                               'UML:Multiplicity'


class TaggedValueExtractor(ModelElementExtractor):

    extractClass = TaggedValue

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['dataValue'] = 'UML:TaggedValue.dataValue/node()'
        self['type'] = 'UML:TaggedValue.type/UML:TagDefinition/@xmi.idref'


class DataTypeExtractor(ModelElementExtractor):

    extractClass = DataType


class ClassifierExtractor(ModelElementExtractor):

    featureNames = []
    dependenciesName = []

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['visibility'] = '@visibility'
        self['isLeaf'] = '@isLeaf'
        self['isAbstract'] = '@isAbstract'

        items = []
        for name in self.featureNames:
            items.append('UML:Classifier.feature/' + name)
        self['feature'] = string.join(items, '|') 

        items = []
        for name in self.dependenciesName:
            items.append('UML:ModelElement.clientDependency/' + name + \
                         '/@xmi.idref')

        self['clientDependency'] = string.join(items, '|')
        self['generalization'] = 'UML:GeneralizableElement.generalization/' + \
                                 'UML:Generalization/@xmi.idref'


class ClassExtractor(NamespaceExtractor, ClassifierExtractor):

    elementNames = ['UML:Class', 'UML:StateMachine', 'UML:ActivityGraph']
    featureNames = ['UML:Attribute', 'UML:Operation', 'UML:Method']
    dependenciesName = ['UML:Abstraction', 'UML:Dependency']
    extractClass = Class

    def __init__(self):

        NamespaceExtractor.__init__(self)
        ClassifierExtractor.__init__(self)


class FeatureExtractor(ModelElementExtractor):

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['visibility'] = '@visibility'
        self['ownerScope'] = '@ownerScope'


class AttributeExtractor(FeatureExtractor):

    typeNames = ['UML:DataType', 'UML:Class', 'UML:Interface']
    extractClass = Attribute

    def __init__(self):

        FeatureExtractor.__init__(self)

        items = []
        for name in self.typeNames:
            items.append('UML:StructuralFeature.type/' + name + '/@xmi.idref')
        self['type'] = string.join(items, '|') 

        self['changeability'] = '@changeability'
        self['initialValue'] = 'UML:Attribute.initialValue/UML:Expression'
        self['multiplicity'] = 'UML:StructuralFeature.multiplicity/' + \
                               'UML:Multiplicity'


class MultiplicityExtractor(ModelElementExtractor):

    extractClass = Multiplicity

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['range'] = 'UML:Multiplicity.range/UML:MultiplicityRange'


class MultiplicityRangeExtractor(ModelElementExtractor):

    extractClass = MultiplicityRange

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['lower'] = '@lower'
        self['upper'] = '@upper'


class OperationExtractor(FeatureExtractor):

    extractClass = Operation

    def __init__(self):

        FeatureExtractor.__init__(self)

        self['isAbstract'] = '@isAbstract'
        self['isQuery'] = '@isQuery'
        self['isLeaf'] = '@isLeaf'
        self['parameter'] = 'UML:BehavioralFeature.parameter/UML:Parameter'


class ParameterExtractor(ModelElementExtractor):

    typeNames = ['UML:DataType', 'UML:Class', 'UML:Interface']
    extractClass = Parameter

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['kind'] = '@kind'

        items = []
        for name in self.typeNames:
            items.append('UML:Parameter.type/' + name + '/@xmi.idref')
        self['type'] = string.join(items, '|') 

        self['defaultValue'] = 'UML:Parameter.defaultValue/UML:Expression'


class MethodExtractor(FeatureExtractor):

    extractClass = Method

    def __init__(self):

        FeatureExtractor.__init__(self)

        self['body'] = 'UML:Method.body/UML:ProcedureExpression'
        self['specification'] = 'UML:Method.specification/' + \
                                'UML:Operation/@xmi.idref'


class ExpressionExtractor(ModelElementExtractor):

    extractClass = Expression

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['body'] = '@body'
        self['language'] = '@language'


class ProcedureExpressionExtractor(ExpressionExtractor):

    extractClass = ProcedureExpression


class InterfaceExtractor(ClassifierExtractor, NamespaceExtractor):

    featureNames = ['UML:Operation']
    elementNames = ['UML:Class', 'UML:Interface']
    dependenciesName = ['UML:Abstraction', 'UML:Dependency']
    extractClass = Interface

    def __init__(self):

        ClassifierExtractor.__init__(self)
        NamespaceExtractor.__init__(self)

class GeneralizationExtractor(ModelElementExtractor):

    classifierNames = ['UML:Class', 'UML:Interface']
    extractClass = Generalization

    def __init__(self):

        ModelElementExtractor.__init__(self)

        items = []
        for name in self.classifierNames:
            items.append('UML:Generalization.child/' + name + '/@xmi.idref')
        self['child'] = string.join(items, '|')

        items = []
        for name in self.classifierNames:
            items.append('UML:Generalization.parent/' + name + '/@xmi.idref')
        self['parent'] = string.join(items, '|')


class AssociationExtractor(ModelElementExtractor):

    extractClass = Association

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['connection'] = 'UML:Association.connection/UML:AssociationEnd'


class AssociationEndExtractor(ModelElementExtractor):

    classifierNames = ['UML:Class', 'UML:Interface']
    extractClass = AssociationEnd

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['multiplicity'] = 'UML:AssociationEnd.multiplicity/' + \
                               'UML:Multiplicity'

        items = []
        for name in self.classifierNames:
            items.append('UML:AssociationEnd.participant/' + name +
                         '/@xmi.idref')
        self['participant'] = string.join(items, '|')

        self['visibility'] = '@visibility'
        self['changeability'] = '@changeability'
        self['isNavigable'] = '@isNavigable'
        self['targetScope'] = '@targetScope'
        self['aggregation'] = '@aggregation'


class DependencyExtractor(ModelElementExtractor):

    classifierNames = ['UML:Class', 'UML:Interface']
    extractClass = Dependency

    def __init__(self):

        ModelElementExtractor.__init__(self)

        items = []
        for name in self.classifierNames:
            items.append('UML:Dependency.client/' + name + '/@xmi.idref')
        self['client'] = string.join(items, '|')

        items = []
        for name in self.classifierNames:
            items.append('UML:Dependency.supplier/' + name + '/@xmi.idref')
        self['supplier'] = string.join(items, '|')


class AbstractionExtractor(DependencyExtractor):

    extractClass = Abstraction


class CallEventExtractor(ModelElementExtractor):

    extractClass = CallEvent

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['operation'] = 'UML:CallEvent.operation/UML:Operation/@xmi.idref'


class TimeEventExtractor(ModelElementExtractor):

    extractClass = TimeEvent

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['when'] = 'UML:TimeEvent.when/UML:TimeExpression'


class TimeExpressionExtractor(ExpressionExtractor):

    extractClass = TimeExpression


class StateMachineExtractor(ModelElementExtractor):

    # Nota aqui podria ir cualquier subclase de State
    topNames = ['UML:CompositeState']
    contextNames = ['UML:Class', 'UML:Operation']
    extractClass = StateMachine

    def __init__(self):

        ModelElementExtractor.__init__(self)

        items = []
        for name in self.contextNames:
            items.append('UML:StateMachine.context/' + name + '/@xmi.idref')
        self['context'] = string.join(items, '|')

        items = []
        for name in self.topNames:
            items.append('UML:StateMachine.top/' + name)
        self['top'] = string.join(items, '|')

        self['transition'] = 'UML:StateMachine.transitions/UML:Transition'


class StateVertexExtractor(ModelElementExtractor):

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['incoming'] = 'UML:StateVertex.incoming/UML:Transition/@xmi.idref'
        self['outgoing'] = 'UML:StateVertex.outgoing/UML:Transition/@xmi.idref'


class PseudostateExtractor(StateVertexExtractor):

    extractClass = Pseudostate

    def __init__(self):

        StateVertexExtractor.__init__(self)

        self['kind'] = '@kind'


class StateExtractor(StateVertexExtractor):

    actionNames = ['UML:UninterpretedAction', 'UML:ActionSequence',
                   'UML:ReturnAction']

    def __init__(self):

        StateVertexExtractor.__init__(self)

        item = []
        for name in self.actionNames:
            item.append('UML:State.entry/' + name)
        self['entry'] = string.join(item, '|')

        item = []
        for name in self.actionNames:
            item.append('UML:State.doActivity/' + name)
        self['doActivity'] = string.join(item, '|')

        item = []
        for name in self.actionNames:
            item.append('UML:State.exit/' + name)
        self['exit'] = string.join(item, '|')


class CompositeStateExtractor(StateExtractor):

    subvertexNames = ['UML:FinalState', 'UML:SimpleState',
                      'UML:Pseudostate', 'UML:CompositeState',
                      'UML:ActionState']
    extractClass = CompositeState

    def __init__(self):

        StateExtractor.__init__(self)

        item = []
        for name in self.subvertexNames:
            item.append('UML:CompositeState.subvertex/' + name)
        self['subvertex'] = string.join(item, '|')


class SimpleStateExtractor(StateExtractor):

    extractClass = SimpleState


class FinalStateExtractor(StateExtractor):

    extractClass = FinalState


class TransitionExtractor(ModelElementExtractor):

    sourceNames = ['UML:Pseudostate', 'UML:SimpleState', 'UML:CompositeState',
                   'UML:ActionState']
    targetNames = ['UML:Pseudostate', 'UML:SimpleState', 'UML:FinalState',
                   'UML:CompositeState', 'UML:ActionState']
    eventNames = ['UML:CallEvent', 'UML:TimeEvent']
    actionNames = ['UML:ActionSequence', 'UML:UninterpretedAction',
                   'ReturnAction']
    extractClass = Transition

    def __init__(self):

        ModelElementExtractor.__init__(self)

        items = []
        for name in self.sourceNames:
            items.append('UML:Transition.source/' + name + '/@xmi.idref')
        self['source'] = string.join(items, '|')

        items = []
        for name in self.targetNames:
            items.append('UML:Transition.target/' + name + '/@xmi.idref')
        self['target'] = string.join(items, '|')

        items = []
        for name in self.eventNames:
            items.append('UML:Transition.trigger/' + name + '/@xmi.idref')
        self['trigger'] = string.join(items, '|')

        items = []
        for name in self.actionNames:
            items.append('UML:Transition.effect/' + name)
        self['effect'] = string.join(items, '|')

        self['guard'] = 'UML:Transition.guard/UML:Guard'


class GuardExtractor(ModelElementExtractor):

    extractClass = Guard

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['expression'] = 'UML:Guard.expression/UML:BooleanExpression'


class BooleanExpressionExtractor(ExpressionExtractor):

    extractClass = BooleanExpression


class ActionExtractor(ModelElementExtractor):

    def __init__(self):

        ModelElementExtractor.__init__(self)

        self['script'] = 'UML:Action.script/UML:ActionExpression'


class ActionSequenceExtractor(ActionExtractor):

    actionNames = ['UML:ActionSequence', 'UML:UninterpretedAction',
                   'UML:ReturnAction']
    extractClass = ActionSequence

    def __init__(self):

        ActionExtractor.__init__(self)

        items = []
        for name in self.actionNames:
            items.append('UML:ActionSequence.action/' + name)
        self['action'] = string.join(items, '|')


class UninterpretedActionExtractor(ActionExtractor):

    extractClass = UninterpretedAction


class ReturnActionExtractor(ActionExtractor):

    extractClass = ReturnAction


class ActionExpressionExtractor(ExpressionExtractor):

    extractClass = ActionExpression


class ActivityGraphExtractor(StateMachineExtractor):

    extractClass = ActivityGraph


class ActionStateExtractor(SimpleStateExtractor):

    extractClass = ActionState
