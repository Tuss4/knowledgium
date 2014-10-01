# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "shell", inline: "apt-get install -y git python-pip python-virtualenv python-dev libpq-dev vim docker.io"
  config.vm.provision "shell", inline: "ln -sf /usr/bin/docker.io /usr/local/bin/docker"
  config.vm.provision "shell", inline: "sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io"
  config.vm.provision "shell", inline: "groupadd docker && gpasswd -a ${USER} docker"
  config.vm.provision "shell", inline: "serivce docker.io restart && pip install -U fig && pip install fabric"
  config.vm.network "forwarded_port", guest: 5000, host: 8080, auto_correct: true
end
