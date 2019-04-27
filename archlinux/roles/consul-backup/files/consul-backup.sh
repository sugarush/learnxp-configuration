#!/usr/bin/env bash

source /etc/environment

DATE="$(%F+%T)"
SNAPSHOT="/tmp/${DATE}.snap"

consul snapshot save "${SNAPSHOT}"

aws s3 cp "${SNAPSHOT}" "s3://${IDENTIFIER}-${ENVIRONMENT}-consul-backup"
