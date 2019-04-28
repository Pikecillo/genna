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

# Takes a root table of the UML model and builds a dictionary whose
# keys are the xmi.id of the elements: Model, Package, Class, and Inteface;
# and whose values are a list representing its name from the the root of
# the hierarchy of namespaces
def fullNames(table):

    names = {}
    name = []

    def makeNames(namespace):

	# Appends the name of this space to the current name
        name.append(namespace.get('name'))

        # Insert the name of this space into the dictionary
        names[namespace.get('xmi.id')] = name[1:]

        # If the namespace is a Class
        if namespace.__class__ == Class:
	    # Compute the name for each nested Class
            for innerClass in namespace.get('ownedElement', Class).values():
                makeNames(innerClass)

        # If the namespace is a Package
        elif namespace.__class__ in [Model, Package]:

	    # For each classifier or namespace in the package
            for item in [Class, Interface, Model, Package]:
                for element in namespace.get('ownedElement', item).values():
		    # Add the full name to the dictionary
                    makeNames(element)

	# Pop the name of this Package from the current name
        name.pop()

    makeNames(table[table.root_key])

    return names

# Takes the table of elements of a model.
# Returns a dictionary with a list of xmi.id of the opposite ends
# of associations of which each classifier can take part.
# The key is the xmi.if of the classifier and the values are the lists.
def fullAssociations(table):

    associations = {}

    # Initialize the dictionary
    for _id in table.classifiers:
        associations[_id] = ListSet()

    # For each association of the model
    for _id in table.associations:
	# Get the xmi.id of the opposite ends of the association
        actual_ends_id = table[_id].get('connection', AssociationEnd).keys()

	# For each classifier taking part on the association, add the other
	# ends.
        for index in range(len(actual_ends_id)):
            opposites = actual_ends_id[:index] + actual_ends_id[index + 1:]
            classifier_id = table[actual_ends_id[index]].get('participant')
            associations[classifier_id] += opposites

    return associations

# Takes a model element table, a dictionary of namespaces (i.e. returned by
# fullNames), and a dictionary of opposite association ends (i.e. returned by
# fullAssociations).
# Returns a dictionary with the full names of the dependencies of each classifier.
# The following are taken into account: dependencies of the classifier,
# attribute types, operation return types and its parameter types, the interfaces
# it realizes, the classifiers it generalizes, and its associations.
# The values of the dictionary are tuples (element_name, must_be_generated)
def fullOwnDependencies(table, namespaces, associations):

    dependencies = {}
    notForGeneration = nonGeneratedNamespaces(table)

    # Add a dependency. _id is the xmi.id of the dependent element,
    # dep_id is the xmi.id of the dependency element.
    def add(_id, dep_id, generate=True):
        if dep_id in namespaces.keys():
            generated = dep_id not in notForGeneration
            dependencies[_id].append((namespaces[dep_id], generated))

    # Initialize the dictionary
    for _id in table.classifiers:
        dependencies[_id] = ListSet()

        _class = table[_id]

	# Dependencies created by the attributes
        for attribute in _class.get('feature', Attribute).values():
            add(_id, attribute.get('type'))

	# Dependencies created by the operations
        for operation in _class.get('feature', Operation).values():
            for parameter in operation.get('parameter'):
                add(_id, parameter.get('type'))

	# Dependencies created by the generalizations
        for gen_id in _class.get('generalization'):
            add(_id, table[gen_id].get('parent'))

	# Dependencies created by the dependencies (uml.Dependency)
        for dep_id in _class.get('clientDependency'):
            add(_id, table[dep_id].get('supplier'))

        # Dependencies created by the associations
        for end_id in associations[_id]:
            if table[end_id].get('isNavigable') == 'true':
                add(_id, table[end_id].get('participant'))

    return dependencies


# Return a list with the identifiers of all classes and interfaces stereotyped
# as <<utility>>, and of all packages stereotyped as <<framework>>. All the
# classes contained within a <<utility>> class, are also utilities. The
# packages and classes contained within a package <<framework>> are also
# frameworks and utilities, respectively.
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

        # If the namespace is a class and it is labeled as <<utility>> then
        # it enters the list along with all the classes it nests.
        if namespace.__class__ == Class or namespace.__class__ == Interface:
            for _id in namespace.get('stereotype'):
                if table[_id].get('name') == 'utility':
                    addNestedNamespacesRecursively(namespace)

        # If the namespace is a package or model, and it is stereotyped as
        # framework then it enters the list along with all classes or packages
        # it nests.
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
