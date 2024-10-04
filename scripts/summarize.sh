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



DOCS=${TAC}/data/UpdateSumm${TAC_NUMBER}_test_docs_files/
REF=${TAC}/results/UpdateSumm${TAC_NUMBER}_eval/ROUGE/models/
OUTPUT=${ICSISUMM}/output/u${TAC_NUMBER}/

echo "summarize.sh. Will write to ${OUTPUT}"

PYTHONPATH=${PYTHONPATH:-}
export PYTHONPATH=${ICSISUMM}/nltk/nltk-0.9.2:${ICSISUMM}/preprocess/splitta:$PYTHONPATH
PATH=${PATH:-}
export PATH=${ICSISUMM}/solver/glpk-4.43/examples/:$PATH

install -d $OUTPUT

# Clustering (or clusters retrieval
#python ./mcl_cluster.py -i ${DATA}/mcl_clusters_optimised_icsi/ -o ${ICSISUMM}/output/u${TAC_NUMBER}/ #puts in each line of the output file the number of the sentences' cluster
cp ${DATA}/20${TAC_NUMBER}/mcl_clusters_optimised_icsi_AB_glove840b/temp/*-AB.*.97.clus ${OUTPUT}
#cp ${DATA}/20${TAC_NUMBER}/mcl_clusters_optimised_icsi_AB/* ${OUTPUT}
echo "CP DONE !!!!!!!!!!!!!!!!!!!!!"

# Summarizing
export HOSTNAME=localhost
python ${ICSISUMM}/summarizer/inference.py -i ${OUTPUT} -o ${OUTPUT} -t u${TAC_NUMBER} --manpath ${REF} --decoder glpsolve --thresh 0.97 --count 3.0
rm tmp_decoder.*

# To summarize with RST instead of clustering, use /scratch_global/gael/Maali/github-maali-thesis/RST-based-approach/inference_RST_noclust.py called like in run-icsi-primary-sys-34_mcl08_RST_ONO.sh

# To summarize with the initial icsisumm, refer to the comments in inference.py

# Warning: do not distribute ROUGE. It is not freely distributabler

# To use the fusion, generate summaries with base icsisumm, mcl_icsisumm and rst_icsisumm, then use github maali-mnasri/Thesis/fusion

# In fusion: 5 fusion method in .py + best-comb-ROUGE.sh to generate Oracle
# Use each of them to generate fusion results and then use ROUGE to evaluate them and to evaluate also fusion results
