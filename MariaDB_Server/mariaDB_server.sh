#!/bin/bash
echo "cd to /home/centos directory..."
cd /home/centos

echo "installing MariaDB..."
# sudo yum install mysql -y
sudo yum install mariadb-server -y
sudo systemctl start mariadb
sudo systemctl status mariadb
sudo systemctl enable mariadb

echo "Create Database..."
sudo mysql -u root -e "CREATE DATABASE arup;"

echo "update database privileges..."
sudo mysql -u root -e "USE mysql; UPDATE user SET password=PASSWORD('comsc') WHERE User='root' AND Host='localhost'; GRANT ALL PRIVILEGES ON arup.* TO 'root'@'%' IDENTIFIED BY 'comsc'; FLUSH PRIVILEGES;"
