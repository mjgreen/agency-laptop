#!/usr/bin/env bash

# INSTALL for agency

sudo apt install xscreensaver # to prevent getting frozen out by ubuntustudio
sudo apt install libsndfile1-dev portaudio19-dev libportmidi-dev liblo-dev libjack-jackd2-dev # pyo dependencies
sudo apt install libglfw3-dev # glfw windowing backend for psychopy, if wanted
sudo apt install ubuntu-gnome-desktop # fixed 'no sound coming out despite all signs indicating everything was working'

# use gdm3 as window manager
# select "Gnome on X11" from login screen

wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
sh Anaconda3-2019.03-Linux-x86_64.sh

wget https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04/wxPython-4.0.4-cp37-cp37m-linux_x86_64.whl
pip install wxPython-4.0.4-cp37-cp37m-linux_x86_64.whl

git clone git@github.com:belangeo/pyo.git
cd pyo
python setup.py install --use-jack --use-double
cd

git clone git@github.com:psychopy/psychopy.git
cd psychopy
python setup.py install
cd

pip uninstall pyglet
# Successfully uninstalled pyglet-1.4.0b1
pip install pyglet
# Successfully installed pyglet-1.3.2
pip install glfw

git clone git@github.com:mjgreen/agency.git
cd agency/

git clone https://github.com/mjgreen/agency.git
cd agency/
git config credential.helper store # if we are using https instead of ssh

