#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

set -o functrace
failure()
{
  local lineno=$1
  local msg=$2
  echo "Failed at $0, line $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

OUTPUT=${ICSISUMM}/output/u${TAC_NUMBER}/

# Evaluation
install -d ${OUTPUT}/summary_A
rsync -a ${OUTPUT}/summary/*-A ${OUTPUT}/summary_A

install -d ${OUTPUT}/summary_B
rsync -a ${OUTPUT}/summary/*-B ${OUTPUT}/summary_B

python scoring/eval_rouge.py

