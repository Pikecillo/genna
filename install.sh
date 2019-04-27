#!/bin/sh

GENNA_PATH=$PWD
cd $GENNA_PATH/external/PyXML-0.8.4
python setup.py build
python setup.py install
cd $GENNA_PATH/external/4Suite-XML-1.0.2
python setup.py install
cd $GENNA_PATH
