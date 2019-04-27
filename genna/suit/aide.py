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

from uml.element import Model, Package, Class, Interface, \
                        Attribute, Operation, AssociationEnd
from util import ListSet

# Recibe una tabla raiz del modelo UML y construye un diccionario
# cuyas claves son los xmi.id de los elementos: Model,
# Package, Class e Interface y los valores son una lista que
# representa su nombre desde la raiz de la jerarquia de espacios
# de nombre.
def fullNames(table):

    names = {}
    name = []

    def makeNames(namespace):

        # Se agrega el nombre de este espacio al nombre actual
        name.append(namespace.get('name'))

        # Se agrega el nombre de este espacio al diccionario
        names[namespace.get('xmi.id')] = name[1:]

        # Si el espacio de nombre es una clase
        if namespace.__class__ == Class:
            # Se construye el nombre para cada clase anidada.
            for innerClass in namespace.get('ownedElement', Class).values():
                makeNames(innerClass)

        # Si el espacio de nombres es un paquete
        elif namespace.__class__ in [Model, Package]:

            # Por cada classifier o espacio de nombres en el paquete
            for item in [Class, Interface, Model, Package]:
                for element in namespace.get('ownedElement', item).values():
                    # Se agrega el nombre completo al diccionario
                    makeNames(element)

        # Se quita el nombre de este paquete del nombre actual
        name.pop()

    makeNames(table[table.root_key])

    return names

# Recibe la tabla de elementos de un modelo.
# Devuelve un diccionario con una lista de xmi.id de los extremos de
# opuestos de asociaciones en las que participa cada classifier.
# La clave es el xmi.id del classifier y los valores son las listas.
def fullAssociations(table):

    associations = {}

    # Se inicializa el diccionario
    for _id in table.classifiers:
        associations[_id] = ListSet()

    # Por cada asociacion del modelo
    for _id in table.associations:
        # Se obtienen los xmi.id de extremos de la asociacion
        actual_ends_id = table[_id].get('connection', AssociationEnd).keys()

        # Se agregan para cada classifier participante en la asociacion
        # el resto de fines de asociacion
        for index in range(len(actual_ends_id)):
            opposites = actual_ends_id[:index] + actual_ends_id[index + 1:]
            classifier_id = table[actual_ends_id[index]].get('participant')
            associations[classifier_id] += opposites

    return associations

# Recibe una tabla de elementos del modelo, un diccionario de espacios de
# nombre (i.e. el que devuelve fullNames) y un diccionario de fines opuestos
# de asociacion (i. e. el que devuelve fullAssociations).
# Devuelve un diccionario con los nombres completos de las dependencias
# de cada classifier. Para esto se toma en cuenta las dependencias del
# classifier, los tipos de atributos, los tipos devueltos por operaciones
# los tipos de sus parametros, las interfaces que realiza, los classifiers
# que generalice y sus asociaciones.
# Los valors del diccionario son tuplas (nombre_elemento, debe_generarse)
def fullOwnDependencies(table, namespaces, associations):

    dependencies = {}
    notForGeneration = nonGeneratedNamespaces(table)

    # Agrega una dependencia, _id es el xmi.id del elemento
    # dependiente, dep_id es el xmi.id del elemento dependencia
    def add(_id, dep_id, generate=True):
        if dep_id in namespaces.keys():
            generated = dep_id not in notForGeneration
            dependencies[_id].append((namespaces[dep_id], generated))

    # Se inicializa el diccionario
    for _id in table.classifiers:
        dependencies[_id] = ListSet()

        _class = table[_id]

        # Dependencias creadas por los atributos
        for attribute in _class.get('feature', Attribute).values():
            add(_id, attribute.get('type'))

        # Dependencias creadas por las operaciones
        for operation in _class.get('feature', Operation).values():
            for parameter in operation.get('parameter'):
                add(_id, parameter.get('type'))

        # Dependencias creadas por las generalizaciones
        for gen_id in _class.get('generalization'):
            add(_id, table[gen_id].get('parent'))

        # Dependencias creadas por las dependencias (uml.Dependency)
        for dep_id in _class.get('clientDependency'):
            add(_id, table[dep_id].get('supplier'))

        # Dependencias creadas por las asociaciones
        for end_id in associations[_id]:
            if table[end_id].get('isNavigable') == 'true':
                add(_id, table[end_id].get('participant'))

    return dependencies

# Este procedimiento devuelve una lista con los identificadores de todas
# las clases e interfaces estereotipadas como <<utility>> y todos los
# paquetes identificados como <<framework>>. Todas las clases contenidas
# en una clase <<utility>> tambien son clases utility. Los paquetes y clases
# contenidos en un paquete <<framework>> son <<framwork y <<utility>>
# respectivamente.
def nonGeneratedNamespaces(table):

    notForGeneration = []

    def addNestedNamespacesRecursively(namespace):

        notForGeneration.append(namespace.get('xmi.id'))

        for _class in namespace.get('ownedElement', Class).values():
            addNestedNamespacesRecursively(_class)
            
        for interface in namespace.get('ownedElement', Interface).values():
            addNestedNamespacesRecursively(interface)

        if namespace.__class__ == Package or namespace.__class__ == Model:
            for pack in namespace.get('ownedElement', Package).values():
                addNestedNamespacesRecursively(pack)

            for model in namespace.get('ownedElement', Model):
                addNestedNamespacesRecursively(model)

    def identifyNonGenerated(table, namespace):

        # Si el espacio de nombres es una clase y esta etiquetada como
        # <<utility>> entonces entra en la lista junto a todas las clases
        # que anide recursivamente
        if namespace.__class__ == Class or namespace.__class__ == Interface:
            for _id in namespace.get('stereotype'):
                if table[_id].get('name') == 'utility':
                    addNestedNamespacesRecursively(namespace)

        # Si el espacio de nombres es un paquete o modelo y esta etiquetado
        # como <<framework>> entonces entra en la lista junto a todas las
        # clases y paquetes que contenga recursivamente
        if namespace.__class__ == Package or namespace.__class__ == Model:
            for _id in namespace.get('stereotype'):
                if table[_id].get('name') == 'framework':
                    addNestedNamespacesRecursively(namespace)

            for pack in namespace.get('ownedElement', Package).values():
                identifyNonGenerated(table, pack)

            for model in namespace.get('ownedElement', Model).values():
                identifyNonGenerated(table, model)

        for _class in namespace.get('ownedElement', Class).values():
            identifyNonGenerated(table, _class)

        for interface in namespace.get('ownedElement', Interface).values():
            identifyNonGenerated(table, interface)

    identifyNonGenerated(table, table[table.root_key])

    return notForGeneration
