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

# La clase handler recibe un extractor de elemento y el nodo XML
# del que se va a realizar la extraccion. Crea un objeto instancia
# de la clase en uml.element correspondiente y un diccionario en el
# que se indexa dicho elemento y todos sus hijos.

from uml.element import Classifier, Association, Dependency
from xmi.extractor import ExtractorFactory
from xmi.extractor import evaluateXPath, isRecognizedElement

# Diccionario de elementos del modelo
class ElementTable(dict):

    def __init__(self):

        # Clave del elemento raiz del modelo
        self.root_key = None
        # Lista de claves de clasificadores del modelo
        self.classifiers = []
        # Lista de claves de asociaciones del modelo
        self.associations = []
        # Lista de claves de dependencias del modelo
        self.dependencies = []

    # Agrega elemento a la tabla
    def add(self, instance):

        xmi_id = instance.get('xmi.id')
        self[xmi_id] = instance

        # Si el elemento es una asociacion
        # abstraccion o dependencia se agrega a la lista
        # correspondiente.
        if isinstance(instance, Classifier):
            self.classifiers.append(xmi_id)
        elif isinstance(instance, Association):
            self.associations.append(xmi_id)
        elif isinstance(instance, Dependency):
            self.dependencies.append(xmi_id)

    # Actualiza los elementos de la tabla
    def update(self, table):

        dict.update(self, table)
        self.classifiers += table.classifiers
        self.associations += table.associations
        self.dependencies += table.dependencies

class Handler:

    # Constructor recibe un extractor de elemento y el nodo del que
    # se va a extraer el elemento
    def __init__(self, extractor, node):

        # Descomentar para depurar
        extractor.checkAllAttributes()

        # Se crea la tabla de este elemento.
        self.table = ElementTable()

        # Se crea la nueva instancia del elemento que se va a extraer
        ElementClass = extractor.extractClass
        instance = ElementClass(None, None)

        # Por cada atributo del elemento
        for attribute in instance.keys():

            # Averiguo de que caracter es, i. e. si los valores del
            # atributo del elemento son los valores de los nodos
            # extraidos, o son valores compuestos que se deben extraer
            # de los descendientes de dichos nodos
            character = instance.getAttributeCharacter(attribute)

            # Se extrae el nodo que contiene el valor del atributo
            nodes = evaluateXPath(node, extractor[attribute])

            # Si se encontraron nodos
            for otherNode in nodes:

                # Si el valor del nodo es el valor del atributo
                if character == u''.__class__:
                    value = unicode(otherNode.nodeValue)

                # Si se debe seguir buscando el valor
                else:
                    # Se crea la instancia del extractor del elemento
                    factory = ExtractorFactory(otherNode.nodeName)
                    otherExtractor = factory.getExtractorInstance()

                    # Se consigue el valor de el atributo
                    handler = Handler(otherExtractor, otherNode)
                    value = handler.getCreatedInstance()
                    table = handler.getElementTable()

                    # Se actualiza la tabla de este handler
                    self.table.update(table)

                # Se establece el valor del atributo
                instance.set(attribute, value)

        # Se agrega la instancia creada a la tabla
        self.table.add(instance)
        self.table.root_key = instance.get('xmi.id')

    # Devuelve la instancia creada del elemento
    def getCreatedInstance(self):

        return self.table[self.table.root_key]

    # Devuelve la tabla de este elemento
    def getElementTable(self):

        return self.table
