#!/bin/bash

source debian/vars.sh

set -x

# For some reason, CentOS7 builds do not like spaces in filenames
mv 'SourceGuardian Loader License.pdf' SourceGuardian_Loader_License.pdf

echo "PDF"
ls -ld SourceGuardian_Loader_License.pdf

