# Evaluation Scripts for BioCreative VI Precision Medicine Track #

Given gold standard and prediction sets, the Python scripts return
precision, recall and F1 scores for triage and relation tasks.
The current evaluation is based on exact match, which might be changed
in the official run. This early release is to help validate the format
of paritipating teams' prediction sets.

## Public Domain Notice ##

This work is a "United States Government Work" under the terms of the
United States Copyright Act. It was written as part of the authors'
official duties as a United States Government employee and thus cannot
be copyrighted within the United States. The data is freely available
to the public for use. The National Library of Medicine and the U.S.
Government have not placed any restriction on its use or reproduction.

Although all reasonable efforts have been taken to ensure the accuracy
and reliability of the data and its source code, the NLM and the
U.S. Government do not and cannot warrant the performance or results
that may be obtained by using it. The NLM and the U.S. Government
disclaim all warranties, express or implied, including warranties of
performance, merchantability or fitness for any particular purpose.

## Requirements ##

- Python 2.7
- PyBioC (https://github.com/2mh/PyBioC)
- lxml (http://lxml.de)

## How to Use ##

1. Download
  * git clone https://github.com/ncbi-nlp/BC6PM.git

2. Run eval_xml.py (BioC XML) or eval_json.py (BioC JSON)
  * python eval_xml.py [triage|relation] [gold_standard_file] [prediction_file]
  * python eval_json.py [triage|relation] [gold_standard_file] [prediction_file]

## List of Contributors ##

- Rezarta I. Dogan
- Andrew Chatr-aryamontri
- Sun Kim
- Donald C. Comeau
- Zhiyong Lu

## Contact ##

Please contact sun.kim@nih.gov if you have any questions or comments.
