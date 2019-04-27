##======================================================================
##
## Copyright (C) 2007-2019. Mario Rincon Nigro.
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

import string
import sys
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

# Keys [Language name][classifier type]
# Values in tuple list (template name, filename format)
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

# The parameters are:
# -containerPackage: the package with the classifier to be generated
# -directory: output directory. This is were the files with the
# generated code will be written to.
# -language: target language for the code generation.
def generate(containerPackage, directory, language):

    packDirectory = os.path.join(directory, containerPackage['name'])

    # Create the package dir
    if not os.path.isdir(packDirectory):
        try:
            os.makedirs(packDirectory)
        except Exception:
            e = exception.DirectoryCreationError(packDirectory)
            exception.error_handler(e)
            packDirectory = directory

    templateDir = _templatesDir[language]
    generationProfiles = []

    # For each classifier within the package
    for item in ['class', 'interface']:
        for classifier in containerPackage[item]:
            search = [{'class': classifier}, util, settings]

	    # Create the generation profiles. These are tuples with the names list,
	    # the template name, and the name of the source code file, respectively.
            for (templateFilename, sourceCodeNameFormat) in _languageProfile[language][item]:
                template = os.path.join(templateDir, templateFilename)
                filename = os.path.join(packDirectory,
                                        sourceCodeNameFormat % classifier['name'])
                generationProfiles.append((search, template, filename))

    # For each created profile
    for (search, templateFilename, sourceCodeFilename) in generationProfiles:
        print sourceCodeFilename
        if settings.VERBOSE:
            print 'Creating source file ', sourceCodeFilename

        try:
            tmpl = Template(searchList=search, file=templateFilename)
            code = Beautifier(str(tmpl)).getCode()
            output = open(sourceCodeFilename, 'w')
            output.write(code)
            output.close()

        except Exception:
            e = exception.SourceFileCreationError(sourceCodeFilename)
            exception.error_handler(e)

    # For each subpackage
    for package in containerPackage['package'] + containerPackage['model']:

        if 'framework' not in package['stereotype']:
            generate(package, packDirectory, language)


# Call the main function
if __name__ == '__main__':

    # Set default encoding to UTF-8
    reload(sys)
    sys.setdefaultencoding('utf8')

    try:
        print '=== Genna v1.0b1 ==='

        # Parse the arguments
        args = parse(sys.argv[1:])

        print 'Start time:', time.ctime()
        print 'Generating code for model in: %s' % args.input_filename

        # Extract the model
        if settings.STEPS:
            print 'Parsing XMI file...'

        parser = Parser(args.input_filename)
        table = parser.getModelTable()

        # Transform the model
        if settings.STEPS:
            print 'Suitting UML model...'

        rootSuitter = RootModelSuitter(table)
        suittedModel = rootSuitter.getRootModel()

        if settings.STEPS:
            print 'Generating source code...'

	# Create header with all definitions for C++
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

        # Generate source code
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

