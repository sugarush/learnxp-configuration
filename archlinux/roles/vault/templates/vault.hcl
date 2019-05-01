ui = true

storage "consul" {
  address = "{{ lookup('env', 'HOST_IP') }}:8500"
  path = "vault/"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  cluster_address = "{{ lookup('env', 'HOST_IP') }}:8201"
  tls_disable = true
}

api_addr = "http://{{ lookup('env', 'HOST_IP') }}:8200"
cluster_addr = "https://{{ lookup('env', 'HOST_IP') }}:8201"
