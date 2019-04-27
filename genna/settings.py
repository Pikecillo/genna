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

import os
import os.path

# Path hacia este archivo.
GENNA_DIR = os.path.abspath(os.path.dirname(__file__))

# Tipo de generacion
STATIC = '1'
STATE_MACHINES = '2'
ACTIVITY_GRAPHS = '3'
FULL = '4'

# Argumentos por omision.
DEFAULT_GENERATED_CODE_DIR = os.getcwd()
DEFAULT_LANGUAGE = 'cplusplus'
VERBOSE = False
STEPS = False
BEHAVIORAL_GENERATION = FULL

# Ubicacion de las clases bases para maquinas de estado
SMBASE_DIR = os.path.join(GENNA_DIR, 'smbase')

# Ubicacion de las plantillas de codigo
TEMPLATE_DIR = os.path.join(GENNA_DIR, 'templates')
CPLUSPLUS_TEMPLATES_DIR = os.path.join(TEMPLATE_DIR, 'cplusplus')
JAVA_TEMPLATES_DIR = os.path.join(TEMPLATE_DIR, 'java')

