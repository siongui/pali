#!/bin/bash

SDK_DIR=~/google_appengine
APP_DIR=`dirname $0`
DEV_DATASTORE_PATH=${APP_DIR}/GAEDevDatastore

${SDK_DIR}/dev_appserver.py --datastore_path=${DEV_DATASTORE_PATH} ${APP_DIR}
