#!/bin/bash
# meant to be run as root

set +o history
WORKINGDIR=`pwd`
VENAME="bakshi"
VEDIR="$WORKINGDIR/$VENAME"
INSTALL="yum install"
CLIPS_SRC_URL="http://pyclips.sourceforge.net/files/CLIPSSrc.zip"

cd $WORKINGDIR

function finish {
 cd $WORKINGDIR
 set -o history
 echo "-------------------"
 if [ ! -f $WORKINGDIR/python32/bin/python ]; then
   echo "32bit python was not built"
 elif [ ! -d $VEDIR ]; then
   echo "virtualenv $VENAME not created"
 elif [ ! -d $VEDIR/lib/python2.6 ]; then
   echo "32bit python2.6 is not in use in virtualenv"
 elif [ ! -d $VEDIR/lib/python2.6/site-packages/clips ]; then
   echo "clips module not built in virtualenv"
 else
   $VEDIR/bin/python -c "import sys; print(sys.version_info); print(sys.path);"
   $VEDIR/bin/python -c "import clips; print('clips imported successfully')"
   echo "Django verion:"
   $VEDIR/bin/python -c "import django; print(django.get_version())"
 fi
}

trap finish EXIT 

# start python environment if already exists
# else continue with script to build it
#
if [ -f $VEDIR/python32/bin/python2.6 -a -d $VEDIR/lib/python2.6/site-packages/clips ]
 source $VEDIR/bin/activate
fi


# make sure we have needed tools to build 32bit python2.6 and pyclips
yes | $INSTALL python wget unzip tar make gcc
yes | $INSTALL libgcc.{i686,x86_64} glibc-common.{i686,x86_64} glibc-devel.{i686,x86_64} glibc-headers.{i686,x86_64}

# libs needed for virtualenv to create environment
yes | $INSTALL zlib-devel.{i686,x86_64}

# libs needed for pip to be included in new virtualenv environment
yes | $INSTALL readline-devel.{i686,x86_64} openssl-devel.{i686,x86_64}


# build 32bit python in /opt/python32
#
if [ ! -f $WORKINGDIR/python32/bin/python ]; then
 cd $WORKINGDIR
 if [ ! -f "Python-2.6.9.tgz" ]; then
  wget "https://www.python.org/ftp/python/2.6.9/Python-2.6.9.tgz"
 fi
 tar -xzvf Python-2.6.9.tgz
 cd Python-2.6.9
 mkdir $WORKINGDIR/python32
 chmod 775 $WORKINGDIR/python32
 ./configure --prefix=/opt/python32 CC="gcc -m32" CXX="g++ -m32" LD="ld -m elf_i386"
 make
 make install
 chmod -R 755 $WORKINGDIR/python32
 chmod 555 $WORKINGDIR
fi


# isolate system python from the just built 32bit python2.6
#
# note: virtualenv should come with its own pip and setuptools
#
cd $WORKINGDIR
wget "https://pypi.python.org/packages/source/v/virtualenv/virtualenv-12.0.6.tar.gz"
tar xvfz virtualenv-12.0.6.tar.gz
cd virtualenv-12.0.6
# note: using system python to install virtualenv
python setup.py install


# create and enter isolated python environment using 32bit python2.6
cd $WORKINGDIR
virtualenv --python=$WORKINGDIR/python32/bin/python $VENAME


# build pyclips with 32bit python
#
cd $WORKINGDIR
if [ ! -f "${WORKINGDIR}/pyclips-1.0.7.348.tar.gz" ]; then
 wget -O pyclips-1.0.7.348.tar.gz "http://sourceforge.net/projects/pyclips/files/pyclips/pyclips-1.0/pyclips-1.0.7.348.tar.gz/download"
fi
tar xvzf pyclips-1.0.7.348.tar.gz
cd pyclips
if [ ! -f CLIPSSrc.zip ]; then
 echo "getting CLIPSSrc.zip\n"
 wget $CLIPS_SRC_URL
 unzip CLIPSSrc.zip
 mv CLIPSSrc/CLIPSSrc clipssrc
 rm -r CLIPSSrc
 chmod -R 777 clipssrc
fi
# install pyclips into our isolated python environment
$VEDIR/bin/python setup.py install

# install django into our isolated python environment
# note: nothing after django1.6 supports python2.6
$VEDIR/bin/pip install django==1.6

