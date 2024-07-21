cd mavproxy
py setup.py build install --user
cd ..
py move.py
py MAVProxy/MAVProxy/mavproxy.py