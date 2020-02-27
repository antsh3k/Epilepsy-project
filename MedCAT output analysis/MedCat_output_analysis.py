""" Analysing SNOMED annotations from the MedCAT output """

# Import packages
import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from medcat.cdb import CDB
import os


# Load Concept database (CDB) used for the project
cdb = CDB()
cdb.load_dict(os.path.join("/Volumes/NO NAME/", "snomed.dat"))


# Load MedCAT output
file_path = r"/Volumes/NO NAME/"  # add file path
file = r"AShek_project_EXport_MedCAT_Export_With_Text_2020-01-30_16_07_02.json"  # Add file name

with open(file_path + file) as f:
    data = json.load(f)

print("The number of projects is: ", len(data['projects']))  # number of projects

# Read all documents from all projects to doc_df
doc_df = pd.DataFrame([a for d in data['projects'] for a in d['documents']])
print("The number of documents is", len(doc_df['id']))  # number of documents
doc_df['last_modified'] = pd.to_datetime(doc_df['last_modified'])

# Read annotations to ann_df
ann_df = pd.DataFrame([a for c in data['projects'] for b in c['documents'] for a in b['annotations']])
ann_df['last_modified'] = pd.to_datetime(ann_df['last_modified'])

print("The number of deleted annotations is", ann_df[ann_df['deleted']].shape[0])  # Deleted
print("The number of correct annotations is",ending order by a default of concept frequency of 10.
    :param df: Use the ann_df
      ann_df[~ann_df['deleted'] & ~ann_df['alternative'] & ~ann_df['manually_created']].shape[0])  # Correct
print("The number of alternative concepts are", ann_df[ann_df['alternative']].shape[0])  # Alternatives
print("The number of annotations added", ann_df[ann_df['manually_created']].shape[0])  # Add annotation
print("The work each user has done is as follows", ann_df.groupby('user').count())  # participants in exercise

# Write to csv
# ann_df.to_csv(r"C:\Users\k1767582\Documents\GitHub\Epilepsy-project\20200115medcatoutput.csv")


###########################################

df_name = pd.DataFrame(doc_df['annotations'][0])
df_name = df_name.sort_values('start')
pretty_name = []
for index, row in df_name.iterrows():
    value = row["cui"]
    p_name = cdb.cui2pretty_name[value]
    pretty_name.append(p_name)
df_name["Concept_name"] = pretty_name
df_name = df_name[["start", "end", "value", "cui", "Concept_name", "meta_anns"]]


################
def concept_count(df, concepts_freq=10):
    """
    This function will group by concept ID's in desc
    :param concepts_freq:
    :return:
    """
    # Describe Cui
    groups_by_cui = df.groupby('cui')
    # print(list(groups_by_cui))

    # Plot the count of each CUI
    a = groups_by_cui.count()
    a = a.sort_values(by='acc', ascending=False)

    # convert cui to pretty name
    pretty_name = []
    a = a.reset_index()

    for index, row in a.iterrows():
        value = row["cui"]
        p_name = cdb.cui2pretty_name[value]
        pretty_name.append(p_name)
    a["Concept_name"] = pretty_name
    print(a)

    # Filter df by top concept frequency
    a = a[a['acc'] >= concepts_freq]

    # Plot box plot of snomed concept frequency
    x = a["Concept_name"]
    y = a["acc"]
    plt.bar(x, y)
    plt.title("Count of SNOMED concepts >= {}".format(concepts_freq))  # select CUIs with count >= concepts_freq
    plt.xticks(fontsize=10, rotation=25, horizontalalignment="right")
    plt.ylim(bottom=0)
    plt.ylabel("Total Concept Count")
    plt.show()
    return


def total_concept_freq(df):
    """
    :param df: The DataFrame containing the mentions of concepts per document (Use df:doc_df)
    :return: A figure of distribution of all mention concept count per document
    """
    doc_id = []
    concepts = []

    for index, row in df.iterrows():
        temp_df = pd.DataFrame([a for a in row['annotations']])
        for index2, row2 in temp_df.iterrows():
                doc_id.append(index + 1)
                concepts.append(row2["cui"])
    summary_df = pd.DataFrame(columns=["doc_id", "cui"])
    summary_df["doc_id"] = doc_id
    summary_df["cui"] = concepts
    print(summary_df)
    summary_by_doc = summary_df.groupby(['doc_id'])\
        .agg({'cui': 'count'})\
        .rename(columns={'doc_id': 'Cui count'})
    print(summary_by_doc)
    # Plot
    x = summary_by_doc.index
    y = summary_by_doc['cui']

    # Plot cui count per document
    plt.bar(x, y, label="Total: {}".format(x[-1]))
    plt.title("Distribution of Total Concepts Encountered")
    plt.ylabel("Total Concept Count per Document")
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.xlabel("Document Number")
    plt.legend(loc='upper right')
    plt.show()
    return


def new_concept_freq(df):
    """
    :param df: The DataFrame containing the mentions of concepts per document (Use df:doc_df)
    :return: A figure of first mention concept count per document
    """
    doc_id = []
    concepts = []

    for index, row in df.iterrows():
        temp_df = pd.DataFrame([a for a in row['annotations']])
        for index2, row2 in temp_df.iterrows():
            if row2["cui"] not in concepts:
                doc_id.append(index + 1)
                concepts.append(row2["cui"])
            else:
                doc_id.append(index + 1)
                concepts.append(None)
    summary_df = pd.DataFrame(columns=["doc_id", "cui"])
    summary_df["doc_id"] = doc_id
    summary_df["cui"] = concepts
    print(summary_df)
    summary_by_doc = summary_df.groupby(['doc_id'])\
        .agg({'cui': 'count'})\
        .rename(columns={'doc_id': 'Cui count'})
    print(summary_by_doc)
    # Plot
    x = summary_by_doc.index
    y = summary_by_doc['cui']

    # Plot cui count per document
    plt.bar(x, y, label="Total: {}".format(x[-1]))
    plt.title("Distribution of New SNOMED Concepts Encountered")
    plt.ylabel("New Concept Count per Document")
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.xlabel("Document Number")
    plt.legend(loc='upper right')
    plt.show()
    return


def learning_rate_by_cui(df, SNOMED_code, pretty_name=None):
    """This function will return the learning rate for specific SNOMED code. Optional entry by synonym.
    :param df: Use the doc_df
    :param SNOMED_code:
    :param pretty_name:
    :return:
    """
    doc_id = []
    no_correct = []
    value = []
    for index, row in df.iterrows():
        temp_df = pd.DataFrame([a for a in row['annotations']])
        for index, row2 in temp_df.iterrows():
            if row2["cui"] == SNOMED_code:
                doc_id.append(row['id'])
                no_correct.append(row2["correct"])
                value.append(row2["value"])
            else:
                pass
    summary_df = pd.DataFrame(columns=["doc_id", "correct", "value"])
    summary_df["doc_id"] = doc_id
    summary_df["correct"] = no_correct
    summary_df["value"] = value

    # Filter by synonym(pretty_name)
    if pretty_name is None:
        pass
    else:
        summary_df = summary_df[summary_df["value"] == pretty_name]
    print(summary_df)

    # See synonyms
    # TODO something here has gone wrong double check no mention of Levetiracetam or topiramate etc
    by_name = summary_df.groupby(['value'])\
        .agg({'doc_id': 'count', 'correct': 'sum'})\
        .rename(columns={'doc_id': 'Value count', 'correct': 'Correct sum'})
    by_name['Percent Acc'] = by_name['Correct sum']/by_name['Value count'] * 100
    print(by_name)

    # Calculate accuracy per doc
    accuracy_by_doc = summary_df.groupby(["doc_id"]).agg({'correct': 'sum', 'value': 'count'}) \
        .reset_index() \
        .rename(columns={'correct': 'Correct sum', 'value': 'Value count'})
    accuracy_by_doc.index = accuracy_by_doc.index + 1  # shift index +1

    accuracy_by_doc['Percent Acc'] = accuracy_by_doc['Correct sum']/accuracy_by_doc['Value count'] * 100
    print(accuracy_by_doc)

    # Plot
    x = accuracy_by_doc.index
    y = accuracy_by_doc['Percent Acc']
    # Add trend line
    slope, intercept, r_value, p_value, std_err = stats\
        .linregress(x=accuracy_by_doc.index, y=accuracy_by_doc['Percent Acc'])
    r2 = round(r_value**2, 2)
    print("slope={}, intercept={}, r_value={}, p_value={}, std_err={}"
          .format(round(slope, 2), round(intercept, 2), round(r_value, 2), p_value, round(std_err, 2)))
    # plt.plot(x, intercept + slope * x, 'r', label="r$^2$ = {}".format(r2))

    # Plot accuracy for SNOMED concept
    plt.scatter(x, y, marker='o', s=accuracy_by_doc['Value count']+30)

    plt.title("The Learning Rate for {}".format(SNOMED_code))
    plt.ylabel("% Confirmed Accurate")
    plt.ylim(bottom=0, top=110)
    plt.xlabel("Document Count")
    plt.legend(loc='lower right')
    plt.show()
    return


def medcat_lr(df, top_freq_concepts=None):
    """This function will return the learning rate for overall MedCAT performance.
    :param df: Use the doc_df
    :param top_freq_concepts:
    :return:
    """
    # TODO create a top_freq_concepts option
    doc_id = []
    no_correct = []
    value = []
    for index, row in df.iterrows():
        temp_df = pd.DataFrame([a for a in row['annotations']])
        for index, row2 in temp_df.iterrows():
            doc_id.append(row['id'])
            no_correct.append(row2["correct"])
            value.append(row2["value"])
    summary_df = pd.DataFrame(columns=["doc_id", "correct", "value"])
    summary_df["doc_id"] = doc_id
    summary_df["correct"] = no_correct
    summary_df["value"] = value

    # Calculate accuracy value of each grouped synonym
    by_name = summary_df.groupby(['value']) \
        .agg({'doc_id': 'count', 'correct': 'sum'}) \
        .rename(columns={'doc_id': 'Value count', 'correct': 'Correct sum'})
    by_name['Percent Acc'] = by_name['Correct sum'] / by_name['Value count'] * 100
    print(by_name)
    # TODO test if working
    print(by_name[by_name['Percent Acc'] == 0].sort_values(by=['Value count'], ascending=False))

    # Calculate accuracy per doc
    accuracy_by_doc = summary_df.groupby(["doc_id"]).agg({'correct': 'sum', 'value': 'count'}) \
        .reset_index() \
        .rename(columns={'correct': 'Correct sum', 'value': 'Value count'})
    accuracy_by_doc.index = accuracy_by_doc.index + 1  # shift index +1

    accuracy_by_doc['Percent Acc'] = accuracy_by_doc['Correct sum'] / accuracy_by_doc['Value count'] * 100
    # Filter to only show documents with number of annotations > 10
    accuracy_by_doc = accuracy_by_doc[accuracy_by_doc['Value count'] >= 10]
    # Filter erroneous documents with 0 acc
    accuracy_by_doc = accuracy_by_doc[accuracy_by_doc['Percent Acc'] >= 1]
    print(accuracy_by_doc)

    # Plot
    x = accuracy_by_doc.index
    y = accuracy_by_doc['Percent Acc']

    # Add trend line
    slope, intercept, r_value, p_value, std_err = stats\
        .linregress(x, y)
    r2 = round(r_value**2, 2)
    print("slope={}, intercept={}, r_value={}, p_value={}, std_err={}"
          .format(round(slope, 2), round(intercept, 2), round(r_value, 2), p_value, round(std_err, 2)))

    # Plot accuracy
    plt.scatter(x, y, marker='o', s=accuracy_by_doc['Value count'], label="Frequency of annotations")
    plt.plot(x, intercept + slope*x, 'r', label="r$^2$ = {}".format(r2))
    # Format figure layout
    plt.title("MedCAT Learning Rate")
    plt.ylabel("% Confirmed Accurate")
    plt.ylim(bottom=0, top=110)
    plt.xlim(left=0)
    plt.xlabel("Document Number")
    plt.legend(loc='lower right')
    plt.show()
    return


