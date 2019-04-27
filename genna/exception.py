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

import exceptions
import sys
import time

import xml.sax._exceptions


# Modulo de excepciones y manejo de errores.

class NoModelFoundError(Exception):

    def __init__(self, xmi_filename):
        self.filename = xmi_filename


class DirectoryCreationError(Exception):

    def __init__(self, dirname):
        self.directory = xmi_dirname

class SourceFileCreationError(Exception):

    def __init__(self, filename):
        self.sourcefile = filename

class BadElementCompositionError(Exception):

    def __init__(self, attributeName, ownerClass, validClasses):
        self.attribute = attributeName
        self.ownerClass = ownerClass
        self.validClasses = validClasses

    def __str__(self):

        return '\n"' + self.attribute + '" in ' + str(self.ownerClass) + \
               ' must be instance of any of these classes ' + \
               str(self.validClasses)

class NotAModelElementError(Exception):

    pass

class NotASequenceError(Exception):

    pass

class NotAStringError(Exception):

    pass


def error_handler(exc):
    # Interrupcion de teclado
    if exc.__class__ == KeyboardInterrupt:
        print 'Code generation process has been interrupted at', time.ctime()
        sys.exit(1)

    # Salida del sistema
    elif exc.__class__ == SystemExit:
        pass

    # Excepciones generadas por modulo parser
    elif issubclass(exc.__class__, xml.sax._exceptions.SAXException):
        print 'genna: error: ' + str(exc)
        generation_abort()

    elif exc.__class__ == NoModelFoundError:
        print 'genna: error: no UML model found in input file: ', exc.filename
        generation_abort()

    # Excepciones generadas por modulo principal
    elif exc.__class__ == DirectoryCreationError:
        print 'genna: error: impossible to create directory: ', exc.directory 

    elif exc.__class__ == SourceFileCreationError:
        print 'genna: error: impossible to create source file: ', \
              exc.sourcefile
    
    else:
        # print exc.__class__, ' ', exc
        print 'genna: error: check input model for unsupported elements'
        generation_abort()
        

def generation_abort():
    print 'Code generation process aborted at', time.ctime()
    sys.exit(1)
