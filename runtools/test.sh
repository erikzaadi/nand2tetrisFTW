#!/bin/bash
SCRIPT_BASE="$( cd -P "$( dirname "$0" )" && pwd )"
ROOT_DIR="$( readlink -fn ${SCRIPT_BASE}/../ )"
TEST_RUNNER=${ROOT_DIR}/../tools/HardwareSimulator.sh
if [[ $# -eq 0 ]]; then
    FAILED=0
    for FILE in $(ls ./*.tst); do
        echo "Testing $(basename ${FILE})"
        ${TEST_RUNNER} ${FILE}
        if [[ $? -ne 0 ]]; then
            FAILED=1
        fi
    done
    exit ${FAILED}
else
    TEST_FILE=${1%.*}.tst
    ${TEST_RUNNER} ${TEST_FILE}
    exit $?
fi
