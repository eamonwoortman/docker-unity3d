#!/bin/sh
UNITY_OPTIONS="-batchmode -quit -force-opengl -nographics"

E_NOARGS=85
if [ -z "$1" ]
then
 echo "Usage: `basename $0` <unity editor arguments>"
 exit $E_NOARGS
fi

if [ ! -z "$UNITY_USER" ] && [ ! -z "$UNITY_PASSWORD" ]; then
    /app/auto-register.sh
fi

echo "Starting Unity with the following parameters: $UNITY_OPTIONS $@."
sudo xvfb-run --error-file /var/log/xvfb_error.log --server-args="-screen 0 1024x768x24" \
 /opt/Unity/Editor/Unity $UNITY_OPTIONS $@