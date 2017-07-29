FROM ubuntu:16.04
MAINTAINER Eamon Woortman, contact@eamonwoortman.nl

# install required packages
RUN apt-get -qq update && apt-get -qq install -y \ 
    sudo curl gconf-service lib32gcc1 lib32stdc++6 libasound2 libc6 libc6-i386 libcairo2 libcap2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libfreetype6 libgcc1 libgconf-2-4 \
    libgdk-pixbuf2.0-0 libgl1-mesa-glx libglib2.0-0 libglu1-mesa libgtk2.0-0 libnspr4 libnss3 libpango1.0-0 libstdc++6 libx11-6 libxcomposite1 libxcursor1 libxdamage1 libxext6 \ 
    libxfixes3 libxi6 libxrandr2 libxrender1 libxtst6 zlib1g debconf npm xdg-utils lsb-release libpq5 xvfb && \ 
    rm -rf /var/lib/apt/lists/*

ADD scripts /app

# create a user which can start Unity in a non-root mode
RUN echo "unity ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/unity && export USER=unity && useradd -m unity && echo "unity:unity" | chpasswd && adduser unity sudo 

# set the default user and home to the unity user
USER unity
ENV HOME /home/unity
WORKDIR $HOME
   
# create nessesary folders for Unity and move some scripts around
RUN mkdir -p /home/unity/.cache/unity3d && mkdir -p /home/unity/share/unity3d && sudo chmod -R +x /app \ 
    && sudo mv /app/unity-wrapper.sh /usr/local/bin/unity-wrapper.sh \
     && sudo chown unity:unity /app 
 
# download and install the Unity editor
RUN /app/get-unity.sh && sudo dpkg -i --force-not-root /app/unity_editor.deb && \
    rm /app/unity_editor.deb
