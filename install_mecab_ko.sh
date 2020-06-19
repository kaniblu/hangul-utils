#! /bin/bash

MECAB_URL=https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz
MECAB_PATH=/tmp/mecab-ko
MECAB_DIC_URL=https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.1-20150920.tar.gz
MECAB_DIC_PATH=/tmp/mecab-ko-dic
MECAB_DIC_DICDIR=/usr/local/lib/mecab/dic/mecab-ko-dic
AUTOMAKE_PATH=/tmp/automake
AUTOMAKE_VERSION=1.11
export LD_LIBRARY_PATH=/usr/lib:/usr/local/lib:$LD_LIBRARY_PATH

command_exists() {
    type "$1" &> /dev/null ;
}

# mecab-ko
rm -rf $MECAB_PATH $MECAB_PATH.tar.gz
wget $MECAB_URL -O $MECAB_PATH.tar.gz
mkdir -p $MECAB_PATH
tar zxvf $MECAB_PATH.tar.gz -C $MECAB_PATH
cd $MECAB_PATH/*
./configure
sudo make install -j4

# automake
if ! command_exists automake || [ $(automake --version | grep automake | rev | cut -d ' ' -f 1 | rev) != "$AUTOMAKE_VERSION" ]
then
    rm -rf $AUTOMAKE_PATH
    wget http://ftpmirror.gnu.org/automake/automake-${AUTOMAKE_VERSION}.tar.gz -O $AUTOMAKE_PATH.tar.gz
    mkdir -p $AUTOMAKE_PATH
    tar zxvf $AUTOMAKE_PATH.tar.gz -C $AUTOMAKE_PATH
    cd $AUTOMAKE_PATH/automake-${AUTOMAKE_VERSION}
    ./configure
    sudo make install -j4
fi

# mecab-ko-dic
rm -rf $MECAB_DIC_PATH $MECAB_DIC_PATH.tar.gz
wget $MECAB_DIC_URL -O $MECAB_DIC_PATH.tar.gz
mkdir -p $MECAB_DIC_PATH
tar zxvf $MECAB_DIC_PATH.tar.gz -C $MECAB_DIC_PATH
cd $MECAB_DIC_PATH/mecab*
./autogen.sh
./configure
echo "dicdir=${MECAB_DIC_DICDIR}" > /usr/local/etc/mecabrc
sudo make install -j4


