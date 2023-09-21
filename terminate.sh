#!/bin/bash
terminator -p default --geometry 960x1000 -T "target" &
terminator -p default --geometry 960x1000 -T "target" &
terminator -p local-alt --geometry 800x200 -T "clip-monitor" -e "python3 /opt/red-team-tools/clip.py" &
terminator -p local-alt --geometry 800x400 -T "cred-manager" -e "python3 /opt/red-team-tools/cred-manager.py" &
terminator -p local --geometry 960x1000 -T "local" &
terminator -p local-alt -T "bandwidth monitor **LIMIT 300MB***" --geometry 375x125 -e "python3 /opt/red-team-tools/bandwidth.py -n -p 10" &

