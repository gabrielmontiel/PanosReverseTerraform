terraform {
  required_providers {
    panos = {
      source = "paloaltonetworks/panos"
    }
  }
}
provider "panos" {
  hostname = "192.168.1.1"
  username = "admin"
  password = "Gabriel12"
  timeout  = 10
  logging = [
    "action",
    "op",
    "uid",
    "osx_curl"
  ]
  verify_certificate = false
}
