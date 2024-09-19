#!/bin/bash
mitmdump -s /app/test/proxy.py --listen-host 0.0.0.0 --listen-port 9080 -q &
Xvfb :99 -screen 0 1920x1080x24 &
FD_GEOM=1920x1080 X11VNC_SKIP_DISPLAY=:98 x11vnc -ncache 0 -display :99 -bg -usepw -xkb -listen 0.0.0.0 -forever -rfbport $XPORT & 
export DISPLAY=:99 && fluxbox -log fluxbox.log &
DISPLAY=:99 python3 /app/test/runner.py
# DISPLAY=:99 python3 /app/test/runner.py &
# tail -f /dev/null