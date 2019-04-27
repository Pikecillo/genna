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

# Code beautifier. Takes source code in C++, Java, and Cheetah templates, and carries
# out some formatting transformation that improve legibility

import re;
import string;

# List of substitutions
_substitutions = [
    ('[\t\r\f\v]', ''),         # Remove whitespaces other than ' ' or '\n'
    ('\n +', '\n'),             # Remove spaces after new line
    ('^\s*', '\n'),             # Leave empty line at the beginning
    ('\s*$', '\n'),             # Leave empty line at the end
    ('\n{3,}', '\n\n'),         # Remove consecutive empty lines
    (' {2,}', ' '),             # Remove consecutive ' '
    (r'([\w\$]+) +\(', r'\1('), # Remove whitespaces before (
    ('[ \t\r\f\v]*{', ' {'),    # Remove whitespaces before {
    ('{\n+', '{\n'),
    ('\n+}', '\n}'),            # Remove consecutive new lines before }
    (' +;', ';'),               # Remove whitespaces before ;
    (' +,', ','),               # Remove spaces before ,
    (', {2,}', ', '),           # Remove consecutive spaces after ,
    ('\([ \t\r\f\v]*', '('),
    ('[ \t\r\f\v]*\)', ')')
]

_superTotal = 0
_superUser = 0

# This class applies the transformations
class Beautifier:

    def __init__(self, code):

        global _substitutions

        for item in _substitutions:
            code = re.sub(item[0], item[1], code)

        indent = 0
        lines = []

        # The code is first split in lines
        for line in string.split(code, '\n'):

            # If the line is not empty
            if line:
                if re.search('^(public|private|protected):', line):
                    indented = ' ' * (4 * indent - 2) + line
                else:
                    indented = ' ' * 4 * indent + line
                    if '{' in line:
                        indent += 1
                    if '}' in line:
                        indent -= 1
                        indented = ' ' * 4 * indent + line
            else:
                indented = line

            lines.append(indented)

        # countLines(lines)

        self.code = string.join(lines, '\n')

    def getCode(self):

        return self.code


def countLines(linesList):

    inExpression = False

    total = 0
    user = 0
    blanks = 0

    for line in linesList:

        # If the line is empty
        if not re.search('^\s*$|^\s*}\s*$', line):
            if not inExpression:
                if re.search('/\*%_<\*/', line):
                    inExpression = True
                    #blanks += 1
                else:
                    total += 1
            else:
                if re.search('/\*>_%\*/', line):
                    inExpression = False
                    #blanks += 1
                else:
                    total += 1
                    user += 1
        #else:
        #    blanks += 1

    global _superTotal, _superUser

    _superTotal += total
    _superUser += user

    #print 'Raw lines: %d' % len(linesList)
    #print 'Blank lines: %d' % blanks
    print 'Total lines: %d' % total
    print 'Automatically generated lines: %d' % (total - user)
    print 'Automatically generated perc: %f %%' % \
          (float((total - user) * 100) / float(total))
    print 'Incomplete lines: %d' % user
    print 'Incomplete lines perc.: %f %%' % (float(user * 100) / float(total))
    print 'General lines total: %d' % _superTotal
    print 'General automatically generated total: %d' % \
          (_superTotal - _superUser)
    print 'General automatically generated total perc.: %f %%' % \
          (float((_superTotal - _superUser) * 100) / float(_superTotal))
    print 'General incomplete lines total: %d' % _superUser
    print 'General incomplete lines total perc.: %f %%' % \
          (float(_superUser * 100) / float(_superTotal))

def beautifulCheetah(code):

    for item in [('\n +', '\n')]:
        regex = re.compile(item[0])
        code = regex.sub(item[1], code)
        
    indent = 0
    lines = []

    # Split the code in lines
    for line in string.split(code, '\n'):

        # If the line is not empty
        if line:
            indented = ' ' * 4 * indent + line
            if '#for' in line or '#if' in line:
                indent += 1
            elif '#end for' in line or '#end if' in line:
                indent -= 1
                indented = ' ' * 4 * indent + line
            elif '#else if' in line:
                indented = ' ' * 4 * (indent - 1) + line
        else:
            indented = line
                
        lines.append(indented)
                
    code = string.join(lines, '\n')
        
    return code

