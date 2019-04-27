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

import os.path
import string


class ListSet(list):

    def __init__(self):

        list.__init__(self)

    def __iadd__(self, y):

        for item in y:
            self.append(item)

        return self

    def append(self, y):

        if y not in self:
            list.append(self, y)


def join(someList, separator=' '):

    return string.join(someList, separator)

def capitalize(someString):

    return string.upper(someString[:1]) + someString[1:]

def lowerize(someString):

    return string.lower(someString[:1]) + someString[1:]

def upper(someString):

    return string.upper(someString)

def join_path(base, filename):

    return os.path.join(base, filename)

def defined(name):

    try:
        name
        return True

    except Exception:
        return False
