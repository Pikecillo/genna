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

import getopt
import os
import os.path
import string
import sys

import settings


class ArgumentsProfile:

    def __init__(self):

        self.input_filename = ''
        self.language = settings.DEFAULT_LANGUAGE
        self.output_directory = settings.DEFAULT_GENERATED_CODE_DIR


def parse(argv):

    short_options = 'hvsb:l:o:'
    long_options = ['help', 'verbose', 'steps', 'behavioral=', 'language=',
                    'output-directory=']

    try:
        opts, args = getopt.gnu_getopt(argv, short_options, long_options)

    except getopt.GetoptError, error:
        print 'genna: ' + error.msg
        usage()
        print 'Try \'genna --help\' for more information'
        sys.exit(2)

    profile = ArgumentsProfile()

    # Get options
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit()

        if option in ('-v', '--verbose'):
            settings.VERBOSE = True

        if option in ('-s', '--steps'):
            settings.STEPS = True

        if option in ('-b', '--behavioral='):
            if value not in ('1', '2', '3', '4'):
                print 'genna: invalid option for code generation: ', value
                print 'Try \'genna --help\' for more information'
                sys.exit(2)

            settings.BEHAVIORAL_GENERATION = value 

        if option in ('-l', '--language'):
            if value not in ('cplusplus', 'java'):
                print 'genna: not a supported language: ', value
                print 'Supported languages: cpluplus, java'
                print 'Try \'genna --help\' for more information'
                sys.exit(2)

            profile.language = value

        if option in ('-o', '--output-directory'):
            profile.output_directory = value

    # Make sure an input file was specified
    if not args:
        print 'genna: input file not specified'
        usage()
        print 'Try \'genna --help\' for more information'
        sys.exit(2)

    if len(args) > 1:
        print 'codelay: multiple input files specified: ' + \
              string.join(args, ', ')
        print 'Try \'genna --help\' for more information'
        sys.exit(2)

    profile.input_filename = args[0]

    # Check paths exist
    if not os.access(profile.input_filename, os.F_OK):
        print 'genna: input file not found: \'%s\'' % \
              profile.input_filename
        sys.exit(2)

    if not os.access(profile.output_directory, os.F_OK):
        print 'genna: output directory not found: \'%s\'' % \
              profile.output_directory
        sys.exit(2)

    # Check read/write permissions for directories
    if not os.access(profile.output_directory, os.R_OK):
        print 'genna: permission denied for reading: \'%s\'' % \
              profile.input_filename
        sys.exit(2)

    if not os.access(profile.output_directory, os.W_OK):
        print 'genna: permission denied for writting in: \'%s\'' % \
              profile.output_directory
        sys.exit(2)

    # Check input file is a regular file
    if not os.path.isfile(profile.input_filename):
        print 'genna: input file is not a regular file: %s' % \
              profile.input_filename
        sys.exit(2)
    
    return profile
    

def usage():

    print """usage: genna [options] input-file
  options: [[-o | --output-directory=DIRECTORY]
            [-l | --language=LANGUAGE] : LANGUAGE {cplusplus, java}
            [-b | --behavioral=VALUE] : VALUE {1, 2, 3, 4}
            [-v | --verbose]
            [-s | --steps]
            [-h | --help]]
  defaults: --output-directory=./
            --language=cplusplus
            --behavioral=4
    """


def help():

    usage()

    print """  options description:

    -o, --output-directory PATH :
            path to output directory

    -l, --language LANGUAGE :
            target language for code generation process

    -b, --behavioral VALUE :
            behavioral code generation option:
                 1 : generate only static structure
                 2 : generate static structure + state machine implementation
                 3 : generate static structure + activity graphs
                 4 : full

    -v, --verbose :
            show generated source code filenames

    -s, --steps :
            show code generation process steps

    -h, --help :
            show this help
    """

    print "Copyright (C) 2007. Universidad de Los Andes."
