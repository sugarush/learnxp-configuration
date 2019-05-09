import sys

import consul as python_consul
import hvac


consul = python_consul.Consul(host='consul.service.consul')
vault = hvac.Client(url='http://vault.service.consul:8200')

vault.token = '{{ vault_token[lookup('env', 'ENVIRONMENT')] }}'

consul_prefix = 'tsugi/{{ lookup('env', 'DEPLOYMENT') }}'
consul_keys = [ ]
consul_keys_missing = [ ]

vault_mount_point = 'kv'
vault_path = 'tsugi/{{ lookup('env', 'DEPLOYMENT') }}'
vault_keys = [
    'admin_password',
    'database_host',
    'database_name',
    'database_password',
    'database_user',
    'cookie_secret',
    'developer_mode',
    'mail_domain',
    'mail_secret',
    'session_salt',
    'wwwroot'
]
vault_keys_missing = [ ]


def print_missing():

    if consul_keys_missing:
        print('Consul Missing {prefix}/'.format(prefix=consul_prefix))
        for key in consul_keys_missing:
            print(key)

    if vault_keys_missing:
        print('Vault Missing {prefix}/'.format(prefix=vault_path))
        for key in vault_keys_missing:
            print(key)


for key in consul_keys:
    _, value = consul.kv.get('{prefix}/{key}'.format(
        prefix = consul_prefix,
        key = key
    ))
    if value is None:
        consul_keys_missing.append(key)

try:
    vault_data = vault.secrets.kv.v2.read_secret_version(
        path = vault_path,
        mount_point = vault_mount_point
    )
except hvac.exceptions.InvalidPath:
    print_missing()
    print('Vault Missing Path: {path}/'.format(path=vault_path))
    sys.exit(2)

for key in vault_keys:
    if key not in vault_data['data']['data']:
        vault_keys_missing.append(key)

if consul_keys_missing or vault_keys_missing:
    print_missing()
    sys.exit(2)
