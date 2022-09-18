#!/bin/bash
cd /home/centos

# This scripts creates all the folders currently needed to
# store the CSV's produced by the application
# It then sets Permissions on all folders to full read and write access for everyone

# ADD Inputs Folders
mkdir -m 777 /home/centos/CSO
mkdir -m 777 /home/centos/QUBE
mkdir -m 777 /home/centos/NRFA
mkdir -m 777 /home/centos/DO
mkdir -m 777 /home/centos/BOD+NH3
# END INPUT FOLDERS

# Graphs Folders
mkdir -m 777 /home/centos/BOD_GRAPH
mkdir -m 777 /home/centos/NH3_GRAPH

# Outputs Folder
mkdir -m 777 /home/centos/OUTPUT

# Images Folder
mkdir -m 777 /home/centos/IMAGES

# Documentation Folder
mkdir -m 777 /home/centos/DOCS
