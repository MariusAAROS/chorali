#!/bin/bash

set -o errexit
set -o pipefail
# set -o functrace


if [[ "x${DIR}" == "x" ]]; then
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
fi
set -o nounset

failure()
{
  local lineno=$1
  local msg=$2
  echo "Failed at $0, line $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR


#exemple $1 = 2003
input=$1
output=$2
#input=$1
#foutput=$2
rm -rf $output
mkdir $output
#for min in 0.3 0.325 0.35 0.375 0.4 0.425 0.45 0.475 0.5 0.525 0.55 0.575 0.6 0.625 0.65 0.675 0.7 0.725 0.75 0.775 0.8 0.825 0.85 0.875 0.9 0.925 0.95 0.96 0.97 0.98 0.99
#for min in 0.2 0.3 0.33 0.35 0.37 0.4 0.43 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
for min in 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 0.3 0.35 0.4 0.45 0.5 0.55 0.96 0.97 0.98 0.99
#for min  in 0.96 0.97 0.98 0.99
do
	out=$output/$min
	mkdir $out
	python ${DIR}/summarizer/filterSimABC.py -i $input -m $min -o $out
done
