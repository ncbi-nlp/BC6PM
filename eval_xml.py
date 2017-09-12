#!/usr/bin/env python

### Collect gold standard and predicted annotations from BioC &
### Compute classification performance scores

import sys

sys.path.append('/home/skim01/PyBioC/src') # Add the path to PyBioC src
import bioc

def BioC_Document(document):
    id = document.id

    if len(document.infons) == 0:
        label = 'no'
    else:
        label = document.infons['relevant']
        label = label.lower()

    return id, label, document.relations

def BioC_Collection_Triage(collection):
    positives = set()
    negatives = set()

    for document in collection.documents:
        id, label, relations = BioC_Document(document)
        if label == 'yes':
            positives.add(id)
        else:
            negatives.add(id)
    return positives, negatives

def Classification_Performance_Triage(collection, gold_standard_positive, gold_standard_negative):
    correct = prediction_count = 0
    precision = recall = f1 = 0

    for document in collection.documents:
        id, label, relations = BioC_Document(document)
        if label == 'yes':
            if id in gold_standard_positive:
                correct += 1.
            prediction_count += 1.

    if prediction_count > 0 and correct > 0 and len(gold_standard_positive) > 0:
        precision = correct / prediction_count
        recall = correct / len(gold_standard_positive)
        f1 = 2. * precision * recall / (precision + recall)
    
    return precision, recall, f1

def BioC_Collection_Relation(collection):
    all_relations = set()
 
    for document in collection.documents:
        id, label, relations = BioC_Document(document)
        for relation in relations:
            relation_flag = 0
            infon_values = []

            for infon_type in relation.infons:
                infon_type_lowercase = infon_type.lower()
                if infon_type_lowercase == 'relation':
                    relation_flag = 1
                elif infon_type_lowercase[:4] == 'gene':
                    infon_values.append(relation.infons[infon_type])

            if relation_flag == 1:
                infon_values.sort()
                relation_string = 'PMID' + id + '_' + '_'.join(infon_values)
                all_relations.add(relation_string)

    return all_relations

def Classification_Performance_Relation(collection, gold_standard_relations):
    correct = prediction_count = 0
    precision = recall = f1 = 0

    for document in collection.documents:
        id, label, relations = BioC_Document(document)
        for relation in relations:
            relation_flag = 0
            infon_values = []

            for infon_type in relation.infons:
                infon_type_lowercase = infon_type.lower()
                if infon_type_lowercase == 'relation':
                    relation_flag = 1
                elif infon_type_lowercase[:4] == 'gene':
                    infon_values.append(relation.infons[infon_type])

            if relation_flag == 1:
                infon_values.sort()
                relation_string = 'PMID' + id + '_' + '_'.join(infon_values)
                if relation_string in gold_standard_relations:
                    correct += 1.
                prediction_count += 1.

    if prediction_count > 0 and correct > 0 and len(gold_standard_relations) > 0:
        precision = correct / prediction_count
        recall = correct / len(gold_standard_relations)
        f1 = 2. * precision * recall / (precision + recall)
    
    return precision, recall, f1

program_name = subtask = gold_standard_file = prediction_file = None
if len(sys.argv) == 4:
    program_name, subtask, gold_standard_file, prediction_file = sys.argv
else:
    sys.exit('Usage: ' + sys.argv[0] + ' [triage|relation] [gold_standard_file] [prediction_file]')

if subtask != 'triage' and subtask != 'relation':
    sys.exit('Usage: ' + sys.argv[0] + ' [triage|relation] [gold_standard_file] [prediction_file]')

gold_standard_reader = bioc.BioCReader(gold_standard_file)
gold_standard_reader.read()
prediction_reader = bioc.BioCReader(prediction_file)
prediction_reader.read()

if subtask == 'triage':
    gold_standard_positive, gold_standard_negative = BioC_Collection_Triage(gold_standard_reader.collection)
    precision, recall, f1 = Classification_Performance_Triage(prediction_reader.collection, gold_standard_positive, gold_standard_negative)
else:
    gold_standard_relations = BioC_Collection_Relation(gold_standard_reader.collection)
    precision, recall, f1 = Classification_Performance_Relation(prediction_reader.collection, gold_standard_relations)

print('Precision: %.4f' % precision)
print('Recall: %.4f' % recall)
print('F1: %.4f' % f1)