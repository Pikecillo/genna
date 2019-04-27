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

# Parser de XMI

import xml.sax._exceptions

from xml.dom.ext.reader.Sax2 import FromXmlStream

import exception

from xmi.extractor import ExtractorFactory, evaluateXPath
from xmi.handler import Handler


class XMIDocument:

    def __init__(self, filename):

        self.filename = filename

        # Se chequea que el documento de entrada este bien formado
        try:
            xmi = FromXmlStream(filename)

        except Exception, e:
            exception.error_handler(e)

        self.header = evaluateXPath(xmi.documentElement, 'XMI.header')
        self.contentModel = evaluateXPath(xmi.documentElement,
                                          'XMI.content/UML:Model')

    def getHeader(self):

        return self.header

    def getContentModel(self):

        return self.contentModel


# Recibe el nombre de un documento XMI y lo parsea
class Parser:

    def __init__(self, xmiFilename):

        document = XMIDocument(xmiFilename)

        # Saco los elementos UML:Model hijos de XMI.content
        modelNode = document.getContentModel()

        # Si no se consiguio ningun modelo en el contenido
        # del documento XMI
        if not modelNode:
            raise exception.NoModelFoundError(xmiFilename)

        modelNode = modelNode[0]

        # Se crea la representacion del modelo UML
        factory = ExtractorFactory(modelNode.nodeName)
        extractor = factory.getExtractorInstance()
        self.modelHandler = Handler(extractor, modelNode)

    def getModelInstance(self):

        return self.modelHandler.getCreatedInstance()

    def getModelTable(self):

        return self.modelHandler.getElementTable()
