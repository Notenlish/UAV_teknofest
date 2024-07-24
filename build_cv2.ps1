py -m venv cv2-env
cd cv2-env
Scripts/activate
git clone --recursive https://github.com/skvark/opencv-python.git
cd opencv-python
export CMAKE_ARGS="-DWITH_GSTREAMER=ON"
# pip install --upgrade pip wheel
pip wheel . --verbose
# pip install opencv_python*.whl
# note, wheel may be generated in dist/ directory, so may have to cd first

# usta bu tam çalışınca garip bi temp konuma whl dosyasını kaydediyo
#  pip install opencv_python-4.10.0.84-cp311-cp311-win_amd64.whl --force-reinstall
# force reinstall yapınca oluyo

