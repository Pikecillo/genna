#!/bin/sh

GENNA_PATH=$PWD

install_externals() {
	cd $GENNA_PATH/external/PyXML-0.8.4
	python setup.py build
	python setup.py install
	cd $GENNA_PATH/external/4Suite-XML-1.0.2
	python setup.py install
	cd $GENNA_PATH
}

create_exec_script() {
	EXEC_SCRIPT="genna.sh"

	if [ ! -f $EXEC_SCRIPT ]
	then
		echo "#!/bin/sh" >> $EXEC_SCRIPT
		echo "python genna/genna.py \$*" >> $EXEC_SCRIPT
	fi

	chmod +x $EXEC_SCRIPT
}

install_externals
create_exec_script

