variable "flavor" { default = "m1.xlarge" }
variable "image" { default = "CentOS 8 Stream 20210603" }
#variable "instance" { default = "tf_instance" }

variable "name" { default = "Maria DB Server" }

variable "network" { default = "default" }   # you need to change this

variable "keypair" { default = "maria_db_keypair" } # you need to change this
variable "pool" { default = "cscloud_private_floating" }
variable "server_script" { default = "./mariaDB_server.sh" }
variable "security_description" { default = "Terraform security group" }
variable "security_name" { default = "tf_security_maria_db_server" }
