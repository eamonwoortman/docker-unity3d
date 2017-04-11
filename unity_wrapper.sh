#!/bin/sh
UNITY_OPTIONS="-batchmode -quit"

E_NOARGS=85
if [ -z "$1" ]
then
 echo "Usage: `basename $0` <unity editor arguments>"
 exit $E_NOARGS
fi

xvfb-run --error-file /var/log/xvfb_error.log --server-args="-screen 0 1024x768x24" \
 /opt/Unity/Editor/Unity $UNITY_OPTIONS $@