# Chorali

This is the _Chorali summarization system_ of CEA LIST. _Chorali_ is an
evolution of the ICSI summarization system at TAC'09 (licensed under
the GPL v3). _Chorali_ is released under the AGPL v3 license.

## Dependencies

Make sure you have python3.9 installed

- Embeddings, Glove by default. Put the binary file in `$TAC/Embeddings`,
  `$TAC` being defined in `setenv.sh`.
- NLTK, see below
- monolingual-word-aligner: clone chorali with `--recurse-submodules` to obtain it
- Several python requirements:
```
$ pip install -r requirements.txt
```
- Data from NIST, see below
- ROUGE evaluation software, see below
- mcl: `apt install mcl`
Download and install NLTK downloader and then download corpora/stopwords
```
$ python
>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('punkt')
>>> nltk.download('punkt_tab')
```

- Download and setup splitta (see `preprocess/README`)
- Download and setup the data from NIST (see `data/README`)
- Rebuild GLPK (see `solver/README`)


## Usage
Edit `setenv.sh` to adapt it to you environment.

run `./whole-chain.sh` (`sbatch ./whole-chain.sh` if you are working on a cluster with Slurm).

Patient.

If you need to run again some parts, you can comment out previous ones and particularly the similarity computation to save a lot of time.

get the output from `./output/u08`

## Done

* Replaced Perl-based ROUGE-1.5.5 by (Py-rouge)[https://github.com/Diego999/py-rouge]
