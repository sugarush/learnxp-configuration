ui = true

storage "consul" {
  address = "consul.service.consul:8500"
  path = "vault/"
}

listener "tcp" {
  address = "{{ lookup('env', 'HOST_IP') }}:8200"
  tls_disable = true
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = true
}
