#!/bin/bash

set +o nounset
export LD_LIBRARY_PATH=${DIR}/solver/glpk-4.43/src/.libs:${LD_LIBRARY_PATH}

# set -o functrace
failure()
{
  local lineno=$1
  local msg=$2
  echo "Failed at $0, line $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

if [[ "x${DIR}" == "x" ]]; then
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
fi
echo "DIR: $DIR" 1>&2

case $- in
*i*)    # interactive shell
  ;;
*)      # non-interactive shell
  set -o errexit
  set -o pipefail
  set -o nounset
  ;;
esac


# TAC: Original NIST data. Read only
# export TAC=/scratch_global/gael/tac2008
export TAC=${DIR}/data/tac2008
export MN=${DIR}/data/data/multi-news-original-20241022T112859Z-001
export DUC=${DIR}/data/duc2004/task5
ls ${TAC} >& /dev/null

# DATA: Directory for working on TAC data
# export DATA=/scratch_global/gael/tac2008-data
#export DATA=${DIR}/data/tac2008
DATA=${DIR}/data/duc2004/task5
ls ${DATA} >& /dev/null
export DATA=${DATA}

# ICSISUMM: all programs and data included in this distribution
export ICSISUMM=${DIR}
ls ${ICSISUMM} >& /dev/null

# SCRIPTS: the scripts directory in the ICSISUMM distribution
export SCRIPTS=${ICSISUMM}/scripts
ls ${SCRIPTS}  >& /dev/null


export TAC_NUMBER=08
export DUC_NUMBER=04
export SIM_DATA_IN=simABC_icsi_AB_glove840b
export SIM_DATA=allsimABC_icsi_AB_glove840b
export CLUSTERS=mcl_clusters_optimised_icsi_AB_glove840b

# Possibilities for EMBEDDINGS:
# ${PWD}/data/embeddings/GoogleNewsWordnet.bin
# ${PWD}/data/embeddings/glove.840B.300d.bin
# ${PWD}/data/embeddings/frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin

export EMBEDDINGS=${PWD}/data/embeddings/glove.840B.300d.txt
ls ${EMBEDDINGS} >& /dev/null

