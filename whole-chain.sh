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


# conda activate chorali
source ./ilp_sem_venv/bin/activate

set -o errexit
set -o pipefail

set -o functrace
failure()
{
  local lineno=$1
  local msg=$2
  echo "Failed at $0, line $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

DIR=$PWD
if [[ "x${DIR}" == "x" ]]; then
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
fi
echo "DIR: $DIR" 1>&2
set -o nounset


# Set the environment variables necessary, including several parameters
echo "Setting environment" 1>&2
source ${DIR}/setenv.sh

# Preprocessing
echo "Preprocessing" 1>&2
${DIR}/scripts/preprocessing.sh 1>&2

# Compute similarities between sentences using a pre-processed corpus
echo "Computing similarities" 1>&2
${DIR}/scripts/compute_similarities.sh 1>&2

echo "Filtering similarities" 1>&2
DIR=${DIR} ${DIR}/scripts/filter_similarities.sh 1>&2

# Compute clusters using similarities obtained above
echo "Clustering" 1>&2
DIR=${DIR} ${DIR}/scripts/mcl_optimised_with_params.sh 1>&2

# Compute summaries using icsisumm and clusters obtained above
echo "Summarizing" 1>&2
DIR=${DIR} ${DIR}/scripts/summarize.sh 1>&2

# Evaluate resulting summaries using reference summaries and ROUGE
echo "Evaluating" 1>&2
DIR=${DIR} ${DIR}/scripts/evaluate.sh 1>&2

echo "Whole Chorali chain is over" 1>&2

