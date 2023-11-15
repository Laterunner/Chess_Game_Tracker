#! /bin/bash
echo run2.sh 
# This program is run from cptestx.py (main program) to generate IMAGES from FEM
# usage python3 -"FEN"
# clear
# cd ~/Desktop/pyprojects/csr-jet/chess_state_recognition

# script to run fen-to-image
cd fen-to-png
python3 main.py $1

