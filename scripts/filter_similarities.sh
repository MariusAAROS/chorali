#!/bin/bash 

#PBS -N compute_similarities
#PBS -q workq
#PBS -M gael.de-chalendar@cea.fr
#PBS -o out_compute_similarities
#PBS -e err_compute_similarities

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

out=${DATA}/20${TAC_NUMBER}/${SIM_DATA_IN}
out2=${DATA}/20${TAC_NUMBER}/${SIM_DATA}
rm -rf out2
install -d $out2
${SCRIPTS}/filter_by_similarity.sh $out $out2

