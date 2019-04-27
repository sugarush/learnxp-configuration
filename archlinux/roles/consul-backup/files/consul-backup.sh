#!/usr/bin/env bash

source /etc/environment

DATE="$(%F+%T)"
FILE="/tmp/${DATE}.snap"

consul snapshot save "${FILE}"

aws s3 cp "${FILE}" "s3://${IDENTIFIER}-${ENVIRONMENT}-consul-backup"
