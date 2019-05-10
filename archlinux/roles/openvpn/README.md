# OpenVPN Server Configuration

`cd /etc/easy-rsa`

`export EASYRSA=$(pwd)`

`easyrsa init-pki`

Name the CA `openvpn` in the dialog after running the following command.

`easyrsa build-ca`

`cp /etc/easy-rsa/pki/ca.crt /etc/openvpn/server`

`easyrsa gen-req openvpn nopass`

`easyrsa sign-req server openvpn`

`cp /etc/easy-rsa/pki/private/openvpn.key /etc/openvpn/server`

`cp /etc/easy-rsa/pki/issued/openvpn.crt /etc/openvpn/server`

`openvpn --genkey --secret /etc/openvpn/server/ta.key`

`openssl dhparam -out /etc/openvpn/server/dh.pem 2048`

`systemctl start openvpn-server@server`

# OpenVPN Client Certificate

`easyrsa gen-req <name> nopass`

`easyrsa sign-req client <name>`
