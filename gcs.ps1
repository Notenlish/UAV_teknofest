cd mavproxy
py setup.py build install --user
cd ..
py move.py
py MAVProxy/MAVProxy/mavproxy.py --out=udp:127.0.0.1:12945