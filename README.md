##################################
#                                #
#           OCR - DOC            #
#       bartho_c, crouze_t       #
#       mombul_s, wirszt_j       #
#                                #
##################################

# INSTALL PYTHON DEPENDANCIES
sudo apt-get install build-essential
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

# INSTALL PYTHON
wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
tar -xvf Python-2.7.9.tgz
cd Python-2.7.9
./configure
make
sudo make install

# INSTALL PIP
wget https://bootstrap.pypa.io/get-pip.py
chmod +x get-pip.py
python get-pip.py

# INSTALL PROJECT DEPENDANCIES
sudo apt-get install gcc g++ liblas-dev liblapack-dev python-dev gfortran libc6 freetype-dev
pip install numpy
# C'EST LONG.
pip install cv2
# C'EST MOINS LONG.
pip install matplotlib
# C'EST LONG.

# SI ERREUR : "libdc1394" on desactive le driver de la camera (qu'on n'a pas, si on a l'erreur) qu'opencv veut utiliser
sudo ln /dev/null /dev/raw1394

# RUN
./app.py
ou
python app.py

# LE PROGRAMME EST EGALEMENT FONCTIONNEL EN CLI
Usage: python ocr_funcs.py size_x size_y filepath