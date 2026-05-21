provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "monitor_server" {
  ami           = "ami-0f5ee92e2d63afc18"   
  instance_type = "t3.micro"
  key_name      = "Ranjani_1"

  tags = {
    Name = "Monitoring-App-Server"
  }
}

output "public_ip" {
  value = aws_instance.monitor_server.public_ip
}
