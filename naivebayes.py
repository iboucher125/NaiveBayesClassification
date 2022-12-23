import sys
'''
* This program trains a Naive Bayes classifier from a training file
* It makes predictions on an input file (ARFF) which contains independent data 
samples with the same set of features.
'''

# Returns 2 dictionaries of classes and counts from training file
def getData(training_file):
    file = open(training_file, 'r')
    content = file.readlines()
    file.close()
    featureDict = {} # dict that stores attributes and its correcponsing values and counts (dict)
    feature_order = 0 # keeps track of order of attributes
    countDict = {} # dict to store overall count for each class
    data_collection = False
    for line in content:
        if "@attribute" in line:
            raw_line_data = line.split()
            values = [] # list that stores values for each attibute
            
            for i in range(2, len(raw_line_data)):
                # get rid of extra characters
                if "{" in raw_line_data[i]:
                    raw_line_data[i] = raw_line_data[i][1:]
                if "," in raw_line_data[i]:
                    raw_line_data[i] = raw_line_data[i][:len(raw_line_data[i])-1]
                if "}" in raw_line_data[i]:
                    raw_line_data[i] = raw_line_data[i][:len(raw_line_data[i])-1]
                # add attribute value and set count to 0
                values.append(raw_line_data[i])

            # add attribute idx and correspoding value dict
            featureDict[feature_order] = values
            feature_order = feature_order + 1
       
        if data_collection:
            line = line.strip("\n").split(",")
            line_class = line[len(line)-1] # get classification value name
            # update class count
            if line_class in countDict:
                countDict[line_class] += 1
            else:
                countDict[line_class] = 1
            # update value count
            for atribute_idx in range(0, len(line)-1):
                val = line[atribute_idx]
                classDict[line_class][atribute_idx][val] += 1

        if "@data" in line:
            data_collection = True
            class_values = featureDict[len(featureDict)-1]
            del featureDict[len(featureDict)-1] # remove the class attribute from dictionary

            classDict = {} # dictionary that stores class values and correspoinding counts of values in feature dictionary
            for class_type in class_values:
                # create dictonary with possible attribute values and corresponding count
                attrib_dict = {} # keys --> 0, 1, 2, 3
                for attrib_idx in featureDict:
                    temp_val_list = featureDict[attrib_idx] # list of possible values for each attribute
                    # create dictonary that stores count for each possible value for an attribute
                    valueDict = {}
                    for item in temp_val_list:
                        valueDict[item] = 0
                    attrib_dict[attrib_idx] = valueDict
                classDict[class_type] = attrib_dict      
 
    return classDict, countDict

# Write naive bayes results to an output file
def produceOutput(classDict, countDict, total_data, test_file, output_file):
    file = open(test_file, 'r')
    content = file.readlines()
    file.close()
    start_pred = False
    classes = []
    for key in countDict:
        classes.append(key)

    # read through input file
    for line in content:
        # after line with @data -> take that line and write classification and probablities
        if start_pred:
            if line.strip():
                line = line.strip("\n").split(",")
                ans, probs = classify(classDict, countDict, total_data, line)
                # write answer in correct format to output file
                output = ans + " "
                # print(output)
                for item in probs:
                    output += " " + str(item)
                f = open(output_file, "a")
                f.write(output)
                f.close()

        if "@data" in line:
            start_pred = True

# Return classificaiton and list of probabilities
def classify(classDict, countDict, total_data, line):
    # store class with highet probab
    max_prob = 0
    probs = [] # list of probabailities
    for key in countDict:
        curr_prob = (countDict[key]/total_data)
        for i in range(len(line)-1):
            curr_prob *= classDict[key][i][line[i]]/countDict[key]
        probs.append(round(curr_prob, 2))
        if max_prob < curr_prob:
            max_prob = round(curr_prob, 2)
            classification = key
    sum_prob = sum(probs)
    for i in range(len(probs)):
        probs[i] = probs[i]/sum_prob
    return classification, probs

def naiveBayesClassifier(training_file, test_file, output_file):
    # call function to create dictionaries
    classDict, countDict = getData(training_file)
    total_data = 0
    for key in countDict:
        total_data += countDict[key]

    # preform classification on new data and write to output file
    produceOutput(classDict, countDict, total_data, test_file, output_file)


def main():
    training_file = "data/" + sys.argv[1]
    test_file =  "data/" + sys.argv[2]
    output_file = "data/" + sys.argv[3]
    naiveBayesClassifier(training_file, test_file, output_file)
    f = open(output_file, "a")
    f.write("\n")
    f.close()

main()