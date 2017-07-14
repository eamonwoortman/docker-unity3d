#!/bin/bash

export USER=unity

UNITY_LICENSE_FILE=~/.local/share/unity3d/Unity/Unity_v5.x.ulf
MAX_RETRIES=5
COUNTER=0

# patches the unity editor so it doesn't show the EULA agreement window (blocks the automatic login)
sudo python3 /app/idadif.py /opt/Unity/Editor/Unity /app/Unity.dif

while [  $COUNTER -lt $MAX_RETRIES ]; do
    if [ -f $UNITY_LICENSE_FILE ]; then
       break
    fi
        
    echo "Trying to automatically register the license, attept $((COUNTER+1))/$MAX_RETRIES"
    COUNTER=$((COUNTER+1))

    # now patch the launch screen and await the automatic license retrieval process
    python3 /app/patch_unity_launch_screen.py
    
done

# restore the Unity editor
echo "Restoring Unity editor binary"
sudo python3 /app/idadif.py /opt/Unity/Editor/Unity /app/Unity.dif revert
