echo off
clear
# cd /chess_state_recognition

# script to start chess board corner detector
echo ---------------------------------------------------------
echo " environment yoloV8 must be activated in terminal before start"
echo "if not done already type in terminal:"
echo source ~/yoloV8/bin/ activate
echo than rerun this script

echo ---------------------------------------------------------
## cd Desktop/pyprojects/csr/chess_state_recognition
# python3 main.py examples/small_test/0046.png .
python3 main.py ../000image.png .

