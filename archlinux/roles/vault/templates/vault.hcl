ui = true

storage "consul" {
  address = "consul.service.consul:8500"
  path = "vault/"
}

listener "tcp" {
  address = "{{ lookup('env', 'HOST_IP') }}:8200"
  tls_disable = true
}
