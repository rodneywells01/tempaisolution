############################################################
# CMPSC442: Homework 6
############################################################

student_name = "Jason Jincheng Tu"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import email
import collections
import math
import os.path
import operator

############################################################
# Section 1: Spam Filter
############################################################
unknown = "<UNK>"

def load_tokens(email_path):
    contents = []
    message = email.message_from_file(open(email_path, 'r'))
    for lines in email.iterators.body_line_iterator(message):
        for words in lines.split():
            contents.append(words)
    return contents

def log(email_paths, smoothing):
    counter = collections.Counter()
    contents = []
    result = {}
    total = 0  # the amount of words in all files

    # get all the content from the file
    for path in email_paths:
        contents.append(load_tokens(path))

    # counting the word
    for content in contents:
        for word in content:
            counter[word] += 1
        total += len(content)
    total = float(total)

    # calculate the probability
    for word, value in counter.iteritems():
        result[word] = math.log(float(value + smoothing) / (total + smoothing * (len(counter) + 1)))

    result[unknown] = math.log(smoothing / (total + smoothing * (len(counter) + 1)))

    return result, counter, total

#shell function for testing purpose
def log_probs(email_paths, smoothing):
    result, counter, total = log(email_paths, smoothing)
    return result

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        paths = ["%s/%s" % (spam_dir, file) for file in os.listdir(spam_dir)]
        self.spam, spam_counter, total_spam = log(paths, smoothing)
        spam = len(paths)

        paths = ["%s/%s" % (ham_dir, file) for file in os.listdir(ham_dir)]
        self.ham, ham_counter, total_ham = log(paths, smoothing)
        ham = len(paths)

        #the probility for spam email
        temp = float(spam)/(spam+ham)
        self.spamP = math.log(temp)
        self.hamP = math.log(1-temp)

        #for most indicative word calculation
        total = total_ham + total_spam
        indicative = {}
        for word, value in spam_counter.iteritems():
            if word in ham_counter:
                temp = ham_counter[word]
                indicative[word] = math.log((float(value)/total_spam)/(float(value+temp)/total))

        #sort the dictionary
        self.spam_indicative = sorted(indicative.items(), key=operator.itemgetter(1))

    def is_spam(self, email_path):
        content = load_tokens(email_path)
        spamP = self.spamP
        hamP = self.hamP
        counter = collections.Counter()

        #count through the file
        for word in content:
            counter[word] +=1

        #calculate the possibility
        for word, value in counter.iteritems():
            if word in self.spam:
                spamP += (value * self.spam[word])
            else:
                spamP += (value * self.spam[unknown])

            if word in self.ham:
                hamP += (value * self.ham[word])
            else:
                hamP += (value * self.ham[unknown])

        return (spamP > hamP)

    def most_indicative_spam(self, n):
        result = []
        for w, d in self.spam_indicative[n*-1:]:
            result.append(w)
        result.reverse()
        return result


    def most_indicative_ham(self, n):
        result = []
        for w, d in self.spam_indicative[0:n]:
            result.append(w)
        return result

############################################################
# Section 2: Feedback
############################################################


feedback_question_1 = """
8 h
"""

feedback_question_2 = """
when I try to get the accurate result for the possibilty, it is very hard to duplicate the result in the assignment.
If the assignment can give a range of possibility that is acceptable, the assignment will be much better
"""

feedback_question_3 = """
For a program with huge database, I really hope that there are more test data to debug our program.
I made the following lines to provide more data for debugging purpose. If the following data is provided in the assignment, it will help the students a lot

code:
print "words          :\t\tspam\t\tlog\t\t\tindicative\t\tham\t\tlog\t\t\tindicative"
for w in words:
    print "%s:\t\t%d\t\t%f\t\t%f\t\t%d\t\t%f\t\t%f" % (w, spam_counter[w], spam[w], indicative_spam[w], ham_counter[w], ham[w], indicative_ham[w])

results:
words          :		spam		log			indicative		ham		log			indicative
Aug            :		1		-13.008099		-5.157971		266		-6.801268		1.048871
ilug@linux.ie  :		6		-11.216348		-3.991569		493		-6.184255		1.040526
install        :		1		-13.008099		-3.977441		81		-7.990315		1.040353
spam.          :		1		-13.008099		-3.965171		80		-8.002737		1.040201
Group:         :		6		-11.216348		-3.952749		474		-6.223557		1.040044
<a             :		1099		-6.005953		0.428368		1		-12.384754		-5.950442
<input         :		441		-6.919064		0.427013		1		-12.384754		-5.038687
<html>         :		283		-7.362662		0.425751		1		-12.384754		-4.596351
<meta          :		262		-7.439765		0.425468		1		-12.384754		-4.519531
</head>        :		194		-7.740251		0.424137		1		-12.384754		-4.220376
"""
