variable "flavor" { default = "m1.xlarge" }
variable "image" { default = "CentOS 8 Stream 20210603" }

variable "name" { default = "application_server" }

variable "network" { default = "default" }   # you need to change this

variable "keypair" { default = "docker-test" } # you need to change this
variable "pool" { default = "cscloud_private_floating" }
variable "server_script" { default = "./server.sh" }
variable "security_description" { default = "Docker server security group" }
variable "security_name" { default = "tf_docker_diss" }
