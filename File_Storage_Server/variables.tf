variable "flavor" { default = "m1.large" }
variable "image" { default = "CentOS 8 Stream 20210603" }
#variable "instance" { default = "tf_instance" }

variable "name" { default = "File Storage Server" }

variable "network" { default = "default" }   # you need to change this

variable "keypair" { default = "file_storage_keypair" } # you need to change this
variable "pool" { default = "cscloud_private_floating" }
variable "server_script" { default = "./file_storage_server.sh" }
variable "security_description" { default = "Terraform security group" }
variable "security_name" { default = "tf_security_file_storage_server" }
