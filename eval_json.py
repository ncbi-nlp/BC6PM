#!/usr/bin/env python

### Collect gold standard and predicted annotations from BioC &
### Compute classification performance scores

import json
import sys

def JSON_Document(document):
    id = document['id']

    if 'infons' not in document:
        label = 'no'
    else:
        infons = document['infons']
        if 'relevant' in infons:
            label = infons['relevant']
            label = label.lower()
        else:
            label = 'no'

    if 'relations' not in document:
        relations = []
    else:
        relations = document['relations']
    return id, label, relations

def JSON_Collection_Triage(collection):
    positives = set()
    negatives = set()

    for document in collection.get('documents', []):
        id, label, relations = JSON_Document(document)
        if label == 'yes':
            positives.add(id)
        else:
            negatives.add(id)
    return positives, negatives

def Classification_Performance_Triage(collection, gold_standard_positive, gold_standard_negative):
    correct = prediction_count = 0

    for document in collection.get('documents', []):
        id, label, relations = JSON_Document(document)
        if label == 'yes':
            if id in gold_standard_positive:
                correct += 1.
            prediction_count += 1.

    precision = correct / prediction_count
    recall = correct / len(gold_standard_positive)
    f1 = 2. * precision * recall / (precision + recall)
    
    return precision, recall, f1

def JSON_Collection_Relation(collection):
    all_relations = set()
 
    for document in collection.get('documents', []):
        id, label, relations = JSON_Document(document)
        for relation in relations:
            if 'infons' in relation:
                relation_flag = 0
                infon_values = []

                infons = relation['infons']
                for infon_type in infons:
                    infon_type_lowercase = infon_type.lower()
                    if infon_type_lowercase == 'relation':
                        relation_flag = 1
                    elif infon_type_lowercase[:4] == 'gene':
                        infon_values.append(infons[infon_type])

                if relation_flag == 1:
                    infon_values.sort()
                    relation_string = 'PMID' + id + '_' + '_'.join(infon_values)
                    all_relations.add(relation_string)

    return all_relations

def Classification_Performance_Relation(collection, gold_standard_relations):
    correct = prediction_count = 0

    for document in collection.get('documents', []):
        id, label, relations = JSON_Document(document)
        for relation in relations:
            if relation in relations:
                if 'infons' in relation:
                    relation_flag = 0
                    infon_values = []

                    infons = relation['infons']
                    for infon_type in infons:
                        infon_type_lowercase = infon_type.lower()
                        if infon_type_lowercase == 'relation':
                            relation_flag = 1
                        elif infon_type_lowercase[:4] == 'gene':
                            infon_values.append(infons[infon_type])
            
                    if relation_flag == 1:
                        infon_values.sort()
                        relation_string = 'PMID' + id + '_' + '_'.join(infon_values)
                        if relation_string in gold_standard_relations:
                            correct += 1.
                        prediction_count += 1.

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

gold_standard_collection = prediction_collection = None

with open(gold_standard_file) as f1, open(prediction_file) as f2:
    gold_standard_collection = json.load(f1)
    prediction_collection = json.load(f2)

    if subtask == 'triage':
        gold_standard_positive, gold_standard_negative = JSON_Collection_Triage(gold_standard_collection)
        precision, recall, f1 = Classification_Performance_Triage(prediction_collection, gold_standard_positive, gold_standard_negative)
    else:
        gold_standard_relations = JSON_Collection_Relation(gold_standard_collection)
        precision, recall, f1 = Classification_Performance_Relation(prediction_collection, gold_standard_relations)

    print('Precision: %.4f' % precision)
    print('Recall: %.4f' % recall)
    print('F1: %.4f' % f1)