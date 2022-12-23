# NaiveBayesClassification
## Summary
This project includes a Python implemntaiton of a Naive Bayes classifier and an evaluation of the classifier.

## Components
* naivebayes.py - This program trains a Naive Bayes classifier from a ARFF training file and produces and output file containing classifications and probabilities.

Below is an example of how to run this program:
```
python3 naivebayes.py sampletraining.arff sampleinput.arff predictions.txt
```

* evaluate.py - This program implements a leave-one-out-cross-validation using naivebayes.py. It gernerates and prints a confusion matrix and overall accuracy of the classifier. (The classes used in the statistics are hardcoded and must be changed based on the file/data you are using)

Below is an example of how to run this program:
```
python3 evaluate.py contact-lenses.arff
```
