# Genna

Genna is a source code generator for [UML 1.4 models](https://www.omg.org/spec/UML/1.4/About-UML/). Genna is written in
Python, and uses the Cheetah Template Engine for source code generation. The input format for UML models
is [XMI 1.2](https://www.omg.org/cgi-bin/doc?formal/02-01-01).

[ArgoUML](http://argouml.tigris.org/) is recommended for creating the input models, as it supports UML 1.4, and
exports in XMI 1.2.

Genna supports code generation for static structure and dynamic behavior present in UML models. It currently supports
code generation for class hierarchies, state machines in the context of classes, and activity graphs in the context of
class operations. For state machine triggers, only *Call Events* and *Time Events* are currently supported. At the time,
Genna does not validate the correctness of the input models.

The target languages for code generation are C++, and Java.

Genna is written in Python. Genna requires the
[Cheetah Template Engine 0.9.16](http://cheetahtemplate.org/) or superior, and libraries: [PyXML 0.8.4](https://pypi.org/project/PyXML/)
and [4Suite-XML 1.0.2](https://pypi.org/project/4Suite-XML/). Code generated in C++ might need QT library 4.1.2 or superior.

Appropriate versions of those libraries are contained with the project under folder `externals`. Sample models in XMI 1.2 format
are provided within folder `sample_models`.

## Installation

Run `sudo ./install.sh`. This will install PyXML, 4Suite-XML, and generate a run script `genna.sh` that will execute the generator.

## Example usage

Run `./genna.sh sample_models/Tetris_java.xmi -l java -v -o .`

A directory `Tetris` will be created in the current directory. It will contain the source code for the model. Now compile the code, and
run it:

```
cd Tetris
javac *.java __smbase/*.java
java TetrisWindow
```

## References

[Generacion automatica de codigo a partir de maquinas de estado finito. *M. Rincon Nigro,
J. Aguilar Castro, F. Hidrobo Torres*. **Computacion y Sistemas**, 2011](http://www.scielo.org.mx/pdf/cys/v14n4/v14n4a7.pdf) (In Spanish)

[Generacion automatica the codigo fuente en lenguajes orientados a objetos a partir de modelos del UML. *M. Rincon Nigro*.
Mecanografiado de Tesis (Ingenieria de Sistemas) - Universidad de los Andes. Facultad de Ingenieria. Escuela de Sistemas. 2007](https://www.researchgate.net/publication/44471254_Generacion_automatica_de_codigo_fuente_en_lenguajes_orientados_a_objetos_a_partir_de_modelos_del_UML_Mario_Rincon_Nigro) (In Spanish)
