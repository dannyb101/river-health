#!/bin/bash
cd /home/centos
echo in directory $PWD

sudo yum update -y
sudo yum install wget -y
sudo yum install unzip -y
sudo yum install git -y
sudo yum install curl -y

echo "installing gitlab server key..."
sudo touch ~/.ssh/known_hosts
sudo ssh-keyscan git.cardiff.ac.uk >> ~/.ssh/known_hosts
sudo chmod 644 ~/.ssh/known_hosts

echo "Installing Java 11..."
sudo yum update -y
sudo dnf install java-1.8.0-openjdk-devel -y
# sudo yum install openjdk-11-jre -y
sudo yum install default-jdk -y
echo java -version

echo "Installing Python..."
sudo yum -y install epel-release
sudo yum -y update
sudo yum groupinstall "Development Tools" -y
sudo yum install openssl-devel libffi-devel bzip2-devel -y
wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz 
tar xzf Python-3.9.6.tgz 
cd Python-3.9.6
sudo ./configure --with-system-ffi --with-computed-gotos --enable-loadable-sqlite-extensions
./configure --enable-optimizations
sudo make -j ${nproc}
sudo make altinstall
/usr/local/bin/python3.9 -m pip install --upgrade pip

sudo yum update -y
echo python3.9 -V

echo "install Jenkins"
sudo yum update –y
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
sudo yum upgrade
sudo yum install jenkins -y
sudo systemctl daemon-reload
sudo systemctl start jenkins
sudo systemctl status jenkins

echo "installing MariaDB..."
# sudo yum install mysql -y
sudo yum update -y
sudo yum install mariadb-server -y
sudo systemctl start mariadb
sudo systemctl status mariadb
sudo systemctl enable mariadb

sudo mysql -u root -e "USE mysql; UPDATE user SET password=PASSWORD('comsc') WHERE User='root' AND Host='localhost'; GRANT ALL PRIVILEGES ON projectdatabase.* TO 'root'@'localhost' IDENTIFIED BY 'comsc'; FLUSH PRIVILEGES;"

echo "Installing terraform..."
cd /home/centos
wget https://releases.hashicorp.com/terraform/1.1.5/terraform_1.1.5_linux_amd64.zip
unzip terraform_1.1.5_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# remove old docker version if exists
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine            

# add required package repo
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo

# install docker
sudo dnf install docker-ce --nobest -y
sudo systemctl enable --now docker

# add permission to user
sudo usermod -aG docker jenkins
sudo usermod -aG docker $USER
echo "id jenkins: $(id jenkins)"
echo "id user: $(id $USER)"
su -s ${USER}
