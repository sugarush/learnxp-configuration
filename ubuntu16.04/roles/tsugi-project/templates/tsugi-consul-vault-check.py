#!/usr/bin/env python

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
    'apphome',
    'admin_password',
    'auto_approve_keys',
    'bootswatch',
    'bootswatch_color',
    'context_title',
    'cookie_pad',
    'cookie_secret',
    'database',
    'database_password',
    'database_user',
    'data_root',
    'developer_mode',
    'event_check',
    'git_command',
    'google_client_id',
    'google_client_secret',
    'google_map_api_key',
    'google_translate',
    'launch_activity',
    'logo_url',
    'mail_domain',
    'mail_secret',
    'memcache',
    'owner_email',
    'owner_name',
    'provide_keys',
    'service_name',
    'service_description',
    'session_salt',
    'slow_query',
    'timezone',
    'upgrading'
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
