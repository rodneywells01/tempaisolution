############################################################
# CMPSC442: Homework 6
############################################################

student_name = "Rodney Wells"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import os
import email
import math

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    f = open(email_path, 'r')
    message = email.message_from_file(f)

    contents = []
    for line in email.iterators.body_line_iterator(message):
        for word in line.split():
            contents.append(word)

    return contents

def log_probs(email_paths, smoothing):
    count = {}
    total = 0
    for path in email_paths:
        tokens = load_tokens(path)

        for token in tokens:
            if token in count:
                count[token] += 1
            else:
                count[token] = 1
            total += 1

    logvals = {}
    bottomval = total + smoothing * (len(count.keys()) + 1)
    for key in count:
        logvals[key] = math.log((count[key] + smoothing) / bottomval)

    logvals["<UNK>"] = math.log(smoothing / bottomval)

    return logvals


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        # Courtesy http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
        spamfiles = [spam_dir + '/' + file for file in os.listdir(spam_dir) if os.path.isfile(os.path.join(spam_dir, file))]
        hamfiles = [ham_dir + '/' + file for file in os.listdir(ham_dir) if os.path.isfile(os.path.join(ham_dir, file))]
        self.spamdict = log_probs(spamfiles, smoothing)
        self.hamdict = log_probs(hamfiles, smoothing)
        self.pspam = len(spamfiles) * 1.0 / (len(spamfiles) + len(hamfiles))
        self.pham = len(hamfiles) * 1.0 / (len(spamfiles) + len(hamfiles))

    def is_spam(self, email_path):
        hamprob = 0
        spamprob = 0

        tokens = load_tokens(email_path)
        tokencounts = {}
        for token in tokens:
            if token in tokencounts:
                tokencounts[token] += 1
            else:
                tokencounts[token] = 1

        for token in tokencounts:
            if token in self.spamdict:
                spamprob += tokencounts[token] * self.spamdict[token]
            else:
                spamprob += tokencounts[token] * self.spamdict["<UNK>"]

            if token in self.hamdict:
                hamprob += tokencounts[token] * self.hamdict[token]
            else:
                hamprob += tokencounts[token] * self.hamdict["<UNK>"]

        return self.pspam * spamprob > self.pham * hamprob

    def get_best_n(self, scoredict, n):
        """Obtain the best n values from custom dictionary structure"""
        # Obtain best scores
        bestn = []
        bestscores = reversed(sorted(scoredict.keys()))

        for score in bestscores:
            scoringstrings = scoredict[score]
            for beststr in scoringstrings:
                bestn.append(beststr)
                if len(bestn) == n:
                    break

            if len(bestn) == n:
                break

        return bestn

    def generate_score_dictionary(self, category, opposingcategory):
        """Derive a score dictionary based on target category and opposing category"""
        scoredict = {}

        # Generate a score for each value.
        for token in category:
            if token in opposingcategory:
                # Generate score.
                pofw = math.exp(self.spamdict[token]) * self.pspam + math.exp(self.hamdict[token]) * self.pham
                score = category[token] - math.log(pofw)

                # Save score for analysis later.
                if score in scoredict:
                    scoredict[score].append(token)
                else:
                    scoredict[score] = [token]

        return scoredict


    def most_indicative_spam(self, n):
        scoredict = self.generate_score_dictionary(self.spamdict, self.hamdict)
        return self.get_best_n(scoredict, n)


    def most_indicative_ham(self, n):
        scoredict = self.generate_score_dictionary(self.hamdict, self.spamdict)
        return self.get_best_n(scoredict, n)

print "Initializing Spam Filter"
print "========================"
sf = SpamFilter("hw6data/train/spam", "hw6data/train/ham", 1e-5)
print "Initialized"
print "========================"



############################################################
# Section 2: Feedback
########################5####################################

feedback_question_1 = """
I spent about 6 hours on this assignment. It was the easiest one yet!
"""

feedback_question_2 = """
As always, getting acquainted with the concepts and how they actually matter was difficult.
I'm going to continue to review this assignment post completion, as I still don't have a solid
understanding of the concepts introduced.
"""

feedback_question_3 = """
Assignment simplicity was refreshing. Reduced stress and increased my liklihood of revisiting
and tinkering to learn more!
"""
