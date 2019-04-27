Genna is a source code generator for UML 1.4 models. Genna is written in Python, and uses the Cheetah Template Engine
for source code generation. The input format for UML models is XMI 1.2. Genna supports code generation for static
structure and dynamic behavior present in UML models. It currently supports code generation for class hierarchies,
state machines in the context of classes, and activity graphs in the context of class operations. For state machine
triggers, only *Call Events* and *Time Events* are currently supported. At the time, Genna does not validate the
correctness of the input models. The target languages for code generation are C++, and Java. Genna requires the
[Cheetah Template Engine 0.9.16](http://cheetahtemplate.org/) or superior, and libraries: [PyXML 0.8.4](https://pypi.org/project/PyXML/)
and [4Suite-XML 1.0.2](https://pypi.org/project/4Suite-XML/). Code generated in C++ might need QT library 4.1.2 or superior.
