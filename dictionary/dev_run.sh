#!/bin/bash

SDK_DIR=~/google_appengine
APP_DIR=~/dev/pali/dictionary/
DEV_DATASTORE_PATH=~/dev/dicDevStore

${SDK_DIR}/dev_appserver.py --datastore_path=${DEV_DATASTORE_PATH} ${APP_DIR}
