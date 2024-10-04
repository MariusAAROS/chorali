#!/bin/bash -l

# Nombre de machine ou NODES typiquement=1 sauf
#SBATCH -N 1

# Nombre de processus en general=1 (a mémoire distribues type miprun)
#SBATCH --ntasks=1

####SBATCH --gres=cpu

# Nom de votre job afficher dans la lise par squeue
#SBATCH --job-name=chorali

# Nom du fichier de sortie et des erreurs avec l'id du job
##SBATCH --output=out_choralicsi_%j.log
#####SBATCH --error=err_choralicsi_%j.log

#SBATCH --partition=cpu

# Mail pour etre informe de l'etat de votre job
#SBATCH --mail-type=start,end,fail
#SBATCH --mail-user=gael.de-chalendar@cea.fr

# Temps maximal d'execution du job ci dessous
# d-hh:mm:ss
#SBATCH --time=0-4:00:00

# Taille de la memoire exprime en Mega octets max=190000
#SBATCH --mem=20G

####SBATCH --exclude=node5
####SBATCH --nodelist=node6,node7

# This scrip allows to compute the summary of a given cluster of text files

# conda activate chorali
#conda activate maali

set -o errexit
set -o pipefail
# set -o functrace
# set -o xtrace

failure()
{
  local lineno=$1
  local msg=$2
  echo "Failed at $0, line $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ "x${DIR}" == "x" ]]; then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
fi
echo "DIR: $DIR" 1>&2
set -o nounset


# Set the environment variables necessary, including several parameters
echo "Setting environment" 1>&2
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


# ICSISUMM: all programs and data included in this distribution
export ICSISUMM=${DIR}
ls ${ICSISUMM} >& /dev/null

# SCRIPTS: the scripts directory in the ICSISUMM distribution
export SCRIPTS=${ICSISUMM}/scripts
ls ${SCRIPTS}  >& /dev/null


export SIM_DATA_IN=simABC_icsi_AB_glove840b
export SIM_DATA=allsimABC_icsi_AB_glove840b
# export CLUSTERS=mcl_clusters_optimised_icsi_AB_glove840b
export CLUSTERS=mcl_clusters_optimised_icsi_AB_frWak

# Possibilities for EMBEDDINGS:
# ${DATA}/Embeddings/retrofitting/GoogleNewsWordnet.bin
# ${DATA}/Embeddings/GoogleNews-vectors-negative300.bin.gz
# ${DATA}/Embeddings/glove.840B.300d.bin

export EMBEDDINGS=/home/gael/Projets/Newsgene/pychoraliapi/icsisumm_mcl/data/embeddings/glove.6B.300d.txt
# export EMBEDDINGS=/home/gael/Projets/Newsgene/pychoraliapi/icsisumm_mcl/data/embeddings/glove/glove.840B.300d.bin
# export EMBEDDINGS=/home/gael/Projets/Newsgene/pychoraliapi/icsisumm_mcl/data/embeddings/frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin
if [[ "x${EMBEDDINGS}" == "x" ]]; then
    echo "the EMBEDDINGS environment variable must be defined" >&2
    exit 1
fi
ls ${EMBEDDINGS} >& /dev/null

echo "Setting environment OUT" 1>&2

# Preprocessing
echo "Preprocessing" 1>&2
DOCS=${1}
OUTPUT=${2}

echo "Will read ${DOCS}" 1>&2
echo "Will write to ${OUTPUT}" 1>&2

PYTHONPATH=${PYTHONPATH:-}
export PYTHONPATH=${ICSISUMM}/nltk/nltk-0.9.2:${ICSISUMM}/preprocess/splitta:$PYTHONPATH
PATH=${PATH:-}
export PATH=${ICSISUMM}/solver/glpk-4.43/examples/:$PATH

install -d $OUTPUT

# Preprocessing
python ${ICSISUMM}/preprocess/main.py --output $OUTPUT --docpath $DOCS --task chorali --reload --splitta-model ${ICSISUMM}/preprocess/splitta/model_nb/ --is_clean 1>&2

echo "Sentence splitting DONE"  1>&2

# Tokenization
for i in $OUTPUT/*.sent ; do
  echo "Tokenizing $OUTPUT/*.sent" 1>&2
  ${ICSISUMM}/preprocess/penn_treebank_tokenizer.sed $i > $i.tok
done
echo "Tokenization DONE" 1>&2

# Compute similarities between sentences using a pre-processed corpus
echo "Computing similarities" 1>&2

out=${OUTPUT}/${SIM_DATA_IN}
install -d ${out}
minsim=0.0
python ${SCRIPTS}/similarities_lines_AB.py -A $DOCS -e ${EMBEDDINGS} -b True -m $minsim -o $out

echo "Computing similarities DONE" 1>&2

echo "Filtering similarities" 1>&2
out2=${OUTPUT}/${SIM_DATA}
install -d $out2

# for min in 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 0.3 0.35 0.4 0.45 0.5 0.55 0.96 0.97 0.98 0.99
for min in 0.96 0.97 0.98 0.99
do
    install -d $out2/$min
    python ${DIR}/summarizer/filterSimABC.py -i $out -m $min -o $out2/$min
done

# Compute clusters using similarities obtained above
echo "Clustering" 1>&2

output=${OUTPUT}/${CLUSTERS}

install -d ${output}
install -d ${output}/temp

sim_threshold=0.7
files=$(ls ${out2}/${sim_threshold})
for file in $files
do
    echo ${file} 1>&2
    max_nclusters=0
    for output_threshold in 0.96 0.97 0.98 0.99
    do
        echo ${output_threshold} 1>&2
        echo "mcl ${out2}/${output_threshold}/${file}  --abc -o ${output}/temp/${file}${output_threshold}.clus" 1>&2
        mcl ${out2}/${output_threshold}/${file}  --abc -o ${output}/temp/${file}${output_threshold}.clus 1>&2
        echo "mcl endend" 1>&2
        nclusters=$(grep -P '\t' ${output}/temp/${file}${output_threshold}.clus | wc -l) && \
        echo "nclusters $nclusters" 1>&2
        first_cluster=$(head -n 1 ${output}/temp/${file}${output_threshold}.clus | wc -w) && \
        echo "first_cluster ${first_cluster=}" 1>&2
        if [ "$nclusters" -gt "$max_nclusters" ] && [ "$first_cluster" -le 20 ]
        then
            max_nclusters=$nclusters
            opt_clust_file=${output}/temp/${file}${output_threshold}.clus
        fi
    done
    echo "best clus file $opt_clust_file" 1>&2
    cat ${opt_clust_file} > ${output}/${file}.clus
done
echo "Clustering DONE" 1>&2


# Compute summaries using icsisumm and clusters obtained above
echo "Summarizing" 1>&2

# # Clustering (or clusters retrieval
# python ./mcl_cluster.py -i ${DATA}/mcl_clusters_optimised_icsi/ -o ${OUTPUT}/chorali #puts in each line of the output file the number of the sentences' cluster
# echo "Clustering DONE"

# Summarizing
python ${ICSISUMM}/summarizer/inference.py -i ${OUTPUT} -o ${OUTPUT} -t chorali --decoder glpsolve --thresh 0.97 --count 3.0

