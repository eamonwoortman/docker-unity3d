#!/bin/sh
URL=http://download.unity3d.com/download_unity/linux/
PKG=unity-editor-5.5.0f3+20161125_amd64.deb

echo "Downloading Unity3D installer..."
curl -o /app/unity_editor.deb -s "${URL}${PKG}" 
echo "Unity3D installer downloaded."