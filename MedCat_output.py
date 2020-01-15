""" This script deals with analysing the MedCat output """

import json
import pandas as pd


# load the file
file_path = r"C:\Users\k1767582\Documents\GitHub\Epilepsy-project/"
file = r"test_1000 Epilepsy letters.json"


"""

with open(file_path + file) as f:
    data = json.load(f)

print(data.keys())  # Returns a list of keys in a dictionary
# print(data.values())  # returns a list of values in a dictionary


df = json_normalize(data['documents'])
print(df.head(3))
print(df.annotations[8])

df = pd.DataFrame(data)
print(df.head(0))
print(df['documents'].head(1))

print(data2.keys())
df = json_normalize(data2['documents'])
test = df['annotations'][1]
"""

file_path2 = r"E:/"
file2 = "1000 Epilepsy letters_with_text.json"

file_path2 = r"C:\Users\k1767582\Desktop\MedCat output/"
file2 = r"20200110_1000 Epilepsy letters_with_txt.json"

with open(file_path2 + file2) as f:
    data2 = json.load(f)

print("The number of documents is", len(data2['documents']))  # number of documents

df = pd.DataFrame([a for d in data2['documents'] for a in d['annotations']])

print("The number of deleted annotations is", df[df['deleted']].shape[0])  # Deleted
print("The number of correct annotations is",
      df[~df['deleted'] & ~df['alternative'] & ~df['manually_created']].shape[0])  # Correct
print("The number of alternative concepts are", df[df['alternative']].shape[0])  # Alternatives
print("The number of annotations added", df[df['manually_created']].shape[0])  # Add annotation
print("The work each user has done is as follows", df.groupby('user').count())  # participants in exercise

# Describe Cui
groups_by_cui = df.groupby('cui')
print(list(groups_by_cui))
# df.to_csv(r"C:\Users\k1767582\Documents\GitHub\Epilepsy-project\20200114medcatoutput.csv")


# Plot the count of each CUI
import matplotlib.pyplot as plt
a = groups_by_cui.count()
a = a.sort_values(by='acc', ascending=False)

plt.plot(a[a['acc'] >= 5])
plt.title("Count of concepts >= 5")  # select CUIs with count >= 5
plt.xticks(rotation='vertical')
plt.show()


