""" Analysing SNOMED annotations from the MedCAT output """

# Import packages
import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Load MedCAT output
file_path = r"C:\Users\k1767582\Desktop\MedCat output/"
file = r"20200110_1000 Epilepsy letters_with_txt.json"

with open(file_path + file) as f:
    data2 = json.load(f)

print("The number of documents is", len(data2['documents']))  # number of documents

# read document information to doc_df
doc_df = pd.DataFrame.from_dict(data2['documents'])
doc_df['last_modified'] = pd.to_datetime(doc_df['last_modified'])

# read annotations to ann_df
ann_df = pd.DataFrame([a for d in data2['documents'] for a in d['annotations']])
ann_df['last_modified'] = pd.to_datetime(ann_df['last_modified'])

print("The number of deleted annotations is", ann_df[ann_df['deleted']].shape[0])  # Deleted
print("The number of correct annotations is",
      ann_df[~ann_df['deleted'] & ~ann_df['alternative'] & ~ann_df['manually_created']].shape[0])  # Correct
print("The number of alternative concepts are", ann_df[ann_df['alternative']].shape[0])  # Alternatives
print("The number of annotations added", ann_df[ann_df['manually_created']].shape[0])  # Add annotation
print("The work each user has done is as follows", ann_df.groupby('user').count())  # participants in exercise

# Write to csv
# ann_df.to_csv(r"C:\Users\k1767582\Documents\GitHub\Epilepsy-project\20200115medcatoutput.csv")

###########################################


def concept_count(df, concepts_freq=10):
    """This function will group by concept ID's in descending order by a default of concept frequency of 10.
    Use the ann_df
    """
    # Describe Cui
    groups_by_cui = df.groupby('cui')
    print(list(groups_by_cui))

    # Plot the count of each CUI
    a = groups_by_cui.count()
    a = a.sort_values(by='acc', ascending=False)

    plt.plot(a[a['acc'] >= concepts_freq])
    plt.title("Count of concepts >= {}".format(concepts_freq))  # select CUIs with count >= concepts_freq
    plt.xticks(rotation='vertical')
    plt.ylabel("Concept Count")
    plt.show()
    return


def learning_rate_by_cui(df, SNOMED_code, pretty_name=None):
    """This function will return the learning rate for specific SNOMED code. Optional entry by synonym.
    Use the doc_df
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
    by_name = summary_df.groupby(['value'])\
        .agg({'doc_id': 'count', 'correct': 'sum'})\
        .rename(columns={'doc_id': 'Value count', 'correct': 'Correct sum'})
    by_name['Percent Acc'] = by_name['Correct sum']/by_name['Value count'] * 100
    print(by_name)

    # Calculate accuracy per doc
    accuracy_by_doc = summary_df.groupby(["doc_id"]).agg({'correct': 'sum', 'value': 'count'})\
        .reset_index()\
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
          .format(round(slope, 2), round(intercept, 2), round(r_value, 2), round(p_value, 2), round(std_err, 2)))
    plt.plot(x, intercept + slope * x, 'r', label="r$^2$ = {}".format(r2))
    # Plot accuracy for SNOMED concept
    plt.scatter(x, y, marker='x', s=20)

    plt.title("The learning rate for {}".format(SNOMED_code))
    plt.ylabel("% confirmed accurate)")
    plt.ylim(bottom=0, top=110)
    plt.xlabel("Document count")
    plt.legend(loc='right')
    plt.show()
    return


def medcat_lr(df):
    """This function will return the learning rate for overall MedCAT performance.
    """
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
          .format(round(slope, 2), round(intercept, 2), round(r_value, 2), round(p_value, 10), round(std_err, 2)))

    # Plot accuracy

    plt.scatter(x, y, marker='x', s=accuracy_by_doc['Value count'], label=None)
    plt.plot(x, intercept + slope*x, 'r', label="r$^2$ = {}".format(r2))
    # Format figure layout
    plt.title("MedCAT Learning rate")
    plt.ylabel("% confirmed accurate")
    plt.ylim(bottom=0, top=110)
    plt.xlabel("Document count")
    plt.legend(loc='lower right')
    plt.show()
    return
