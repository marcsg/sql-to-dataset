sql-to-dataset converter
==============

Description
--------------
This python script convert XML data exported via SQL Developer to DB Unit dataset format.

Requirements
--------------
libxml2 and lxml are required to run this script. These 2 libraries can be installed as follows:

    brew install libxml2
    sudo pip install lxml

Usage
--------------
    ./sql-to-dataset.py -i input [-t table] [-o output] [-x xslt] [-l]
