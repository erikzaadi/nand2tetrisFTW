#!/bin/bash
SCRIPT_BASE="$( cd -P "$( dirname "$0" )" && pwd )"
ROOT_DIR="$( readlink -fn ${SCRIPT_BASE}/../ )"
SUBMISSION_DIR=${ROOT_DIR}/submissions
PATH_TO_SUBMIT=$(readlink -fn ${1:-${CWD}})
NAME_TO_SUBMIT=$(basename ${PATH_TO_SUBMIT})

if [[ ! -d ${SUBMISSION_DIR} ]]; then
    mkdir -p ${SUBMISSION_DIR}
fi

pushd ${PATH_TO_SUBMIT}

zip ${SUBMISSION_DIR}/project$(expr ${NAME_TO_SUBMIT} + 0).zip ./*.hdl

popd
