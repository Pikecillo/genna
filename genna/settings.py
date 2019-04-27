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

import os
import os.path

# Path to this file
GENNA_DIR = os.path.abspath(os.path.dirname(__file__))

# Code generation mode
STATIC = '1'
STATE_MACHINES = '2'
ACTIVITY_GRAPHS = '3'
FULL = '4'

# Default arguments
DEFAULT_GENERATED_CODE_DIR = os.getcwd()
DEFAULT_LANGUAGE = 'cplusplus'
VERBOSE = False
STEPS = False
BEHAVIORAL_GENERATION = FULL

# Path to base classes for state machines
SMBASE_DIR = os.path.join(GENNA_DIR, 'smbase')

# Path to source code templates
TEMPLATE_DIR = os.path.join(GENNA_DIR, 'templates')
CPLUSPLUS_TEMPLATES_DIR = os.path.join(TEMPLATE_DIR, 'cplusplus')
JAVA_TEMPLATES_DIR = os.path.join(TEMPLATE_DIR, 'java')

