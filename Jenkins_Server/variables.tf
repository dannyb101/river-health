variable "flavor" { default = "m1.large" }
variable "image" { default = "CentOS 8 Stream 20210603" }
#variable "instance" { default = "tf_instance" }

variable "name" { default = "DissServer" }

variable "network" { default = "default" }   # you need to change this

variable "keypair" { default = "dissertation_keys" } # you need to change this
variable "pool" { default = "cscloud_private_floating" }
variable "server_script" { default = "./serverJenkins.sh" }
variable "security_description" { default = "Terraform security group" }
variable "security_name" { default = "tf_security_diss" }
