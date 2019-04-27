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

import sys
import string
import time
import os
import os.path
import distutils.dir_util

from Cheetah.Template import Template

import settings
import util
import exception

from argument import ArgumentsProfile, parse
from xmi.parser import Parser
from suit.suitter import RootModelSuitter
from beautifier import Beautifier


_templatesDir = {'cplusplus': settings.CPLUSPLUS_TEMPLATES_DIR,
                 'java': settings.JAVA_TEMPLATES_DIR
}

_smbaseDir = {'cplusplus': os.path.join(settings.SMBASE_DIR,
                                        'smbaseCpp', '__smbase'),
              'java': os.path.join(settings.SMBASE_DIR,
                                   'smbaseJava', '__smbase')
}

# Claves [Nombre de lenguaje][tipo de classifier]
# Valores lista de tuplas (nombre_template, formato_nombre_archivo)
_languageProfile = {'cplusplus':
                    {'class': [('class_def.cpp.tmpl', '%s.h'),
                               ('class_impl.cpp.tmpl', '%s.cpp')],
                     'interface': [('interface.cpp.tmpl', '%s.h')]
                    },
                    'java':
                    {'class': [('class.java.tmpl', '%s.java')],
                     'interface': [('interface.java.tmpl', '%s.java')]
                    }
}

# Los parametros son el paquete con los classifiers a generar,
# el directorio donde se deben guardar los archivos con el
# codigo fuente y el lenguaje objetivo de la generacion
def generate(containerPackage, directory, language):

    packDirectory = os.path.join(directory, containerPackage['name'])

    # Se crea directorio para paquete
    if not os.path.isdir(packDirectory):
        try:
            os.makedirs(packDirectory)
        except Exception:
            e = exception.DirectoryCreationError(packDirectory)
            exception.error_handler(e)
            packDirectory = directory

    templateDir = _templatesDir[language]
    generationProfiles = []

    # Por cada classifier en este paquete
    for item in ['class', 'interface']:
        for classifier in containerPackage[item]:
            search = [{'class': classifier}, util, settings]

            # Se crean los perfiles de generacion.
            # Estos son tuplas con la lista de nombres, el nombre
            # del template y el nombre del archivo de codigo fuente
            # a crear, en este orden
            for profile in _languageProfile[language][item]:
                template = os.path.join(templateDir, profile[0])
                filename = os.path.join(packDirectory,
                                        profile[1] % classifier['name'])
                generationProfiles.append((search, template, filename))

    # Por cada perfil creado
    for profile in generationProfiles:

        if settings.VERBOSE:
            print 'Creating source file ', profile[2]

        try:
            tmpl = Template(searchList=profile[0], file=profile[1])
            code = Beautifier(str(tmpl)).getCode()
            output = open(profile[2], 'w')
            output.write(code)
            output.close()

        except Exception, ex:
            # print ex.__class__, ' ', ex
            # sys.exit(1)
            e = exception.SourceFileCreationError(profile[2])
            exception.error_handler(e)

    # Por cada subpaquete
    for package in containerPackage['package'] + containerPackage['model']:

        if 'framework' not in package['stereotype']:
            generate(package, packDirectory, language)


# Si se llama desde consola este modulo
if __name__ == '__main__':

    try:
        print '=== Genna v0.1 ==='

        # Se analizan los argumentos
        args = parse(sys.argv[1:])

        print 'Start time:', time.ctime()
        print 'Generating code for model in: %s' % args.input_filename

        # Se extrae el modelo
        if settings.STEPS:
            print 'Parsing XMI file...'

        parser = Parser(args.input_filename)
        table = parser.getModelTable()

        # Se transforma el modelo
        if settings.STEPS:
            print 'Suitting UML model...'

        rootSuitter = RootModelSuitter(table)
        suittedModel = rootSuitter.getRootModel()

        if settings.STEPS:
            print 'Generating source code...'

        # Se crea la cabecera con todas las definiciones para C++
        if args.language == 'cplusplus':
            modelDirectory = os.path.join(args.output_directory,
                                          suittedModel['name'])
            allDefsFilename = os.path.join(modelDirectory,
                                           'all_definitions.h')
            allDefsTmplFilename = os.path.join(_templatesDir['cplusplus'],
                                               'all_def.cpp.tmpl')

            if settings.VERBOSE:
                print 'Creating source file ' + allDefsFilename

            search = [{'package':suittedModel}, util, settings]
            tmpl = Template(searchList=search, file=allDefsTmplFilename)
            code = Beautifier(str(tmpl)).getCode()

            if not os.path.isdir(modelDirectory):
                os.makedirs(modelDirectory)

            output = open(allDefsFilename, 'w')
            output.write(code)
            output.close()

        # Se genera el codigo fuente
        generate(suittedModel, args.output_directory, args.language)

        if suittedModel['hasStateMachine']:

            if settings.STEPS:
                print 'Copying base classes for state machines...'

            distutils.dir_util.copy_tree(_smbaseDir[args.language],
                                         os.path.join(args.output_directory,
                                                      suittedModel['name'], '__smbase'))

        print 'Code generation process completed at', time.ctime()

    except Exception, e:
        exception.error_handler(e)
