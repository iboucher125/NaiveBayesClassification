import sys
import os
''' 
Implements leave-one-out-corss-validation
'''

# Parse input file and return attributes and data
def getContent(input_file):
    file = open(input_file, 'r')
    content = file.readlines()
    file.close()
    attributes = [] # attribute lines
    collect_data = False
    data = []
    for line in content:
        if collect_data == True and "%" not in line:
            data.append(str(line))
        # find lines with attributes -> get written to training file
        if "@attribute" in line:
           attributes.append(line) 
        if "@data" in line:
            collect_data = True
    return attributes, data

# Separate data for cross-validation
def splitData(attributes, data):
    for i in range(len(data)):
        test = data[i]
        if i == 0:
            train = data[i+1:]
        elif i == len(data)-1:
            train = data[:i]
        else:
            train = data[:i-1] + data[i+1:]
        # write to training file
        f = open("training.txt", "w")
        for item in attributes:
            f.write(item)
        f.write("\n")
        f.write("@data\n")
        for item in train:
            f.write(item)
        f.close()
        # write to test file
        f = open("test.txt", "w")
        f.write("@data\n")
        f.write(test + "\n")
        f.write("\n")
        f.close()

        # run naive bayes
        os.system('Python3 naivebayes.py training.txt test.txt result.txt')

def statistics(data):
    # open results file
    file = open("data/result.txt", 'r')
    predictions = file.readlines()
    file.close()
    results = [] # list contraining results
    edited_data = []
    for line in predictions:
        ans = ""
        for character in line:
            if character != " ":
                ans += character
            else:
                break
        results.append(ans)
    for item in data:
        item = item.strip("\n").split(",")
        item = item[len(item)-1]
        edited_data.append(item)

    wrong_count = 0
    final_count = {'none':{'none':0, 'hard':0, 'soft':0}, 'hard':{'none':0, 'hard':0, 'soft':0}, 'soft':{'none':0, 'hard':0, 'soft':0}} # N, H, S
    for i in range(len(edited_data)):
        if edited_data[i] != results[i]:
            wrong_count += 1
        final_count[edited_data[i]][results[i]] += 1
    print("_____________________________________")
    print("KEY: n = none, h = hard, s = soft")
    print("row --> actual; col --> pred")
    print("_____________________________________")
    print("  n  h  s")
    print("----------")
    for key_1 in final_count:
        row = key_1[0] + "|"
        for key_2 in final_count[key_1]:
            row += str(final_count[key_1][key_2]) + " "
        print(row)
    print("_____________________________________")
    print("Overall Accuracy: " + str(len(edited_data) - wrong_count) + "/" + str(len(edited_data)))
    print("_____________________________________")


def main():
    input_file = "data/" + sys.argv[1]
    attributes, data = getContent(input_file)
    splitData(attributes, data)
    statistics(data)

main()