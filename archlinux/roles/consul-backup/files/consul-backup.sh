#!/usr/bin/env bash

source /etc/environment

SNAPSHOT="/tmp/snapshot"

consul snapshot save "${SNAPSHOT}"

aws s3 cp "${SNAPSHOT}" "s3://${IDENTIFIER}-${ENVIRONMENT}-consul-backup"
