#!/bin/bash
#PBS -N mcl
#PBS -q workq
#PBS -M gael.de-chalendar@cea.fr
#PBS -o out_mcl
#PBS -e err_mcl

# This script uses precomputed similarities present in
# ${input}/${sim_threshold} with 'input' computed from environment
# variables and 'sim_threshold' a similarity threshold.
#
# The following environment variables must be defined:
# - DATA The root of all data (input and output);
# - TAC_NUMBER The TAC conference number (e.g.: 08 for TAC 2008);
# - SIM_DATA The folder containing input precomputed similarities;
# - CLUSTERS The subdir where to put resulting clusters;
# - SCRIPTS The scripts folder.

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

input=${DATA}/20${TAC_NUMBER}/${SIM_DATA}
output=${DATA}/20${TAC_NUMBER}/${CLUSTERS}

#rm -rf ${output}
install -d ${output}
install -d ${output}/temp

#python ${SCRIPTS}/online_clustering_w2v.py ${DATA}/20${TAC_NUMBER}/source/ ${DATA}/20${TAC_NUMBER}/semantic_clusters/w2v_0.6/ 0.6

#for sim_threshold in 0.7 0.8 0.76 0.78 #0.82 0.8 0.95 0.9 0.72 0.74 0.76 0.78 0.7 #0.82 0.89 0.86 0.84
for sim_threshold in 0.7
do
    files=$(ls ${input}/${sim_threshold})
    for file in $files
    do
        echo ${file} 1>&2
        max_nclusters=0
        #for th in 0.3 0.325 0.35 0.375 0.4 0.8405 0.45 0.475 0.5 0.525 0.55 0.575 0.6 0.625 0.65 0.675 0.7 0.725 0.75 0.775 0.8 0.825 0.85 0.875 0.9 0.925 0.95 0.96 0.97 0.98 0.99
        #for th in 0.3 0.35 0.4 0.45 0.5 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
        for output_threshold in 0.96 0.97 0.98 0.99
        do
            echo ${output_threshold} 1>&2
	    echo "mcl ${input}/${output_threshold}/${file}  --abc -o ${output}/temp/${file}${output_threshold}.clus" 1>&2
            mcl ${input}/${output_threshold}/${file}  --abc -o ${output}/temp/${file}${output_threshold}.clus 1>&2
            echo "mcl endend" 1>&2
            nclusters=$(grep -P '\t' ${output}/temp/${file}${output_threshold}.clus | wc -l) && \
	    echo "nclusters $nclusters" 1>&2
            first_cluster=$(head -n 1 ${output}/temp/${file}${output_threshold}.clus | wc -w) && \
            echo "first_cluster ${first_cluster=}" 1>&2
            if [ "$nclusters" -gt "$max_nclusters" ] && [ "$first_cluster" -le 10 ]
            then
                max_nclusters=$nclusters
                opt_clust_file=${output}/temp/${file}${output_threshold}.clus
            fi
        done
        echo "best clus file $opt_clust_file" 1>&2
        cat ${opt_clust_file} > ${output}/${file}.clus
    done
done
echo "Clustering DONE" 1>&2

