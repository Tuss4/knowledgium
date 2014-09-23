#!/usr/bin/env bash

apt-get update
apt-get install -y git
apt-get install -y python-pip
apt-get install -y python-virtualenv
apt-get install -y python-dev
apt-get install -y libpq-dev
apt-get install -y vim
apt-get install -y docker.io
ln -sf /usr/bin/docker.io /usr/local/bin/docker
sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io
groupadd docker
gpasswd -a ${USER} docker
service docker.io restart
pip install -U fig
pip install fabric
