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

# Files from A group with one sentence by line and tokenized
inA=${DATA}/20${TAC_NUMBER}/source_alpha_lines_icsi
ls ${inA} > /dev/null
# Files from B group with one sentence by line and tokenized
inB=${DATA}/20${TAC_NUMBER}/source_alpha_lines_icsi_B
ls ${inB} > /dev/null

rm -rf $out
install -d $out


minsim=0.0
# python -m cProfile ${SCRIPTS}/similarities_lines_AB.py -A $inA -B $inB -e ${EMBEDDINGS} -b True -m $minsim -o $out/
python ${SCRIPTS}/similarities_lines_AB.py -A $inA -B $inB -e ${EMBEDDINGS} -b True -m $minsim -o $out/


