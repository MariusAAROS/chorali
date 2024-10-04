import rouge
import os
import re
import sys

def load_system_summaries(dir='./output/u08/summary_A', regex='D08...-A'):
    regex = re.compile(regex)
    system_summaries = {}
    for f in os.scandir(dir):
        if f.is_file() and regex.match(f.name):
            with open(f) as of:
                system_summaries[f.name[:5]] = of.read()
    return system_summaries


def load_reference_summaries(dir='./data/tac2008/results/UpdateSumm08_eval/manual/models', regex='D08..-A.*'):
    regex = re.compile(regex)
    reference_summaries = {}
    for f in os.scandir(dir):
        if f.is_file() and regex.match(f.name):
            if f.name[:5] not in reference_summaries.keys():
                reference_summaries[f.name[:5]] = []
            with open(f) as of:
                reference_summaries[f.name[:5]].append(of.read())
    return reference_summaries


def prepare_results(m, p, r, f):
    return '\t{}:\t{}: {:5.2f}\t{}: {:5.2f}\t{}: {:5.2f}'.format(m, 'P', 100.0 * p, 'R', 100.0 * r, 'F1', 100.0 * f)

system_summaries = load_system_summaries(dir='./output/u08/summary_A', regex='D08...-A')

reference_summaries = load_reference_summaries(dir='./data/tac2008/results/UpdateSumm08_eval/manual/models', regex='D08..-A.*')

all_hypothesis = []
all_references = []

for k in system_summaries.keys():
    if k in reference_summaries.keys():
            all_hypothesis.append(system_summaries[k])
            all_references.append(reference_summaries[k])

#print(f"all_hypothesis\n{all_hypothesis}", file=sys.stderr)
#print(f"all_references\n{all_references}", file=sys.stderr)

#for aggregator in ['Avg', 'Best', 'Individual']:
for aggregator in ['Avg', 'Best']:
    print('Evaluation with {}'.format(aggregator))
    apply_avg = aggregator == 'Avg'
    apply_best = aggregator == 'Best'

    evaluator = rouge.Rouge(metrics=['rouge-n', 'rouge-l', 'rouge-w'],
                           max_n=4,
                           limit_length=True,
                           length_limit=100,
                           length_limit_type='words',
                           apply_avg=apply_avg,
                           apply_best=apply_best,
                           alpha=0.5, # Default F1_score
                           weight_factor=1.2,
                           stemming=True)


    scores = evaluator.get_scores(all_hypothesis, all_references)

    for metric, results in sorted(scores.items(), key=lambda x: x[0]):
        if not apply_avg and not apply_best: # value is a type of list as we evaluate each summary vs each reference
            for hypothesis_id, results_per_ref in enumerate(results):
                nb_references = len(results_per_ref['p'])
                for reference_id in range(nb_references):
                    print('\tHypothesis #{} & Reference #{}: '.format(hypothesis_id, reference_id))
                    print('\t' + prepare_results(metric,results_per_ref['p'][reference_id], results_per_ref['r'][reference_id], results_per_ref['f'][reference_id]))
            print()
        else:
            print(prepare_results(metric, results['p'], results['r'], results['f']))
    print()

