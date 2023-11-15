#! /bin/bash
# This Program is started from main2ext.py to find corner coordinates from image 000image.png
echo off
clear
cd ~/Desktop/pyprojects/csr-jet/chess_state_recognition
# script to start chess board corner detector
echo ---------------------------------------------------------
echo RUNNING ...
echo PLEASE WAIT 10 secs FOR RESULT
echo ---------------------------------------------------------

## cd Desktop/pyprojects/csr/chess_state_recognition
# python3 main.py examples/small_test/0046.png .
python3 main_test.py /home/marius/Desktop/pyprojects/ChessGameTracking/000image.png .
# do not delete the dot in line 13

