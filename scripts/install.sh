#! /bin/bash
sudo yum install -y gcc libjpeg-devel libtiff-devel jasper-devel libpng-devel zlib-devel cmake unzip sqlite-devel readline-devel bzip2-devel openssl-devel ncurses-devel pcre-devel libxslt-devel libxml2-devel mysql mysql-devel
sudo yum install -y yum-priorities
sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
sudo yum install -y eigen3-devel --enablerepo=epel

su -c 'yum localinstall -y --nogpgcheck http://download1.rpmfusion.org/free/el/updates/6/i386/rpmfusion-free-release-6-1.noarch.rpm http://download1.rpmfusion.org/nonfree/el/updates/6/i386/rpmfusion-nonfree-release-6-1.noarch.rpm'
sudo yum install -y ffmpeg-devel

export PYTHON_PREFIX=/usr/local/python-2.7.9

if [ ! -f "Python-2.7.9.tgz" ]; then
    wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
fi

tar -zxvf Python-2.7.9.tgz
cd Python-2.7.9
./configure --enable-shared --prefix=${PYTHON_PREFIX}
make
sudo make install
cd ..
ln -s ${PYTHON_PREFIX} /usr/local/python
sudo cp ${PYTHON_PREFIX}/lib/libpython2.7.so.1.0 /usr/local/lib
sudo ln -s /usr/local/lib/libpython2.7.so.1.0 /usr/local/lib/libpython2.7.so
if [ `grep "/usr/local/lib" /etc/ld.so.conf | wc -l` -eq 0 ];then
    sudo echo "/usr/local/lib" > /etc/ld.so.conf
fi
sudo /sbin/ldconfig
sudo /sbin/ldconfig -v

${PYTHON_PREFIX}/bin/python get-pip.py
${PYTHON_PREFIX}/bin/pip install -r ../requirements.txt

# pyopenssl需要
sudo yum install -y libffi libffi-devel