"""
This script reads json files sort in a selected directory and combines them to a single df and writes the output to a csv
"""

# import necessary packages
import pandas as pd
from pandas.io.json import json_normalize
import json
import random

# load Cogstack output JSON file to convert to DF
filepath = r"C:\Users\k1767582\PycharmProjects\20191025_Epilepsyneurolologyletters\20191101_Epilepsy_dataset\20191101_Epilepsy_clinic_project\Epilepsy_letters_2013_20191001"
filename_2013 = r"cogstack_test_2013.txt"
filename_2014 = r"cogstack_test_2014.txt"
filename_2015 = r"cogstack_test_2015.txt"
filename_2016 = r"cogstack_test_2016.txt"
filename_2017 = r"cogstack_test_2017.txt"
filename_2018 = r"cogstack_test_2018.txt"
filename_201910 = r"cogstack_test_201910.txt"

list_of_JSON_files = [filename_2013, filename_2014, filename_2015, filename_2016, filename_2017, filename_2018, filename_201910]

df = pd.DataFrame()
for filename in list_of_JSON_files:
    f = open(filepath + str("/") + filename)
    s = f.read()
    jsonfile = json.loads(s)
    f.close()
    df_tmp = pd.DataFrame.from_dict(json_normalize(jsonfile["hits"]["hits"]), orient='columns')
    vars()['df_'+filename.replace('.txt','')] = df_tmp
    # eval('df_'+filename.replace('.txt','')) To get the variable
    df = df.append(df_tmp)

df = df.reset_index(drop=True)

# checkout column names
column_names = df.tail(1)
print(column_names) # print column names


# reformat important column dtype
df['_source.documentoutput_doc_dob'] = df['_source.documentoutput_doc_dob'].astype(int)
df['_source.updatetime'] = pd.to_datetime(df['_source.updatetime'])
# df[['_source.client_createdwhen', '_source.client_deceaseddtm', '_source.client_dob', '_source.client_touchedwhen', '_source.clientvisit_closedtm', '_source.clientvisit_createdwhen', '_source.clientvisit_dischargedtm', '_source.clientvisit_planneddischargedtm', '_source.document_dateadded', '_source.document_datecreated', '_source.documentoutput_doc_dob', '_source.updatetime']] = pd.to_datetime(df[['_source.client_createdwhen', '_source.client_deceaseddtm', '_source.client_dob', '_source.client_touchedwhen', '_source.clientvisit_closedtm', '_source.clientvisit_createdwhen', '_source.clientvisit_dischargedtm', '_source.clientvisit_planneddischargedtm', '_source.document_dateadded', '_source.document_datecreated', '_source.documentoutput_doc_dob', '_source.updatetime']], errors='ignore', infer_datetime_format=True)
print(df.info())


# Write complete set of epilepsy documents to_CSV [['_id', '_source.body_analysed']]
# df.to_csv(r"C:\Users\k1767582\PycharmProjects\20191025_Epilepsyneurolologyletters\20191101_Epilepsy_dataset\20191101_Epilepsy_clinic_project\Epilepsy_letters_2013_20191001\complete_epilepsy_clinic.csv", header=True, index=False, escapechar='"')

"""
# This code will select a stratified sample from a dataframe and write to csv
# Set random seed
random.seed(42)

# take a random 1000 sample
selectedrows = df.sample(n=1000, replace=True, random_state=42)
years = ["2013", "2014", "2015", "2016", "2017", "2018", "2019"]
for a in years:
    a = int(a)
    print("For year ", a," there were ", len(selectedrows[selectedrows['_source.updatetime'].dt.year == a]),
          " records.")
selectedrows = selectedrows.reset_index(drop=True)
"""
# write to new csv containing 1000 samples of two columns ['_id', '_source.body_analysed']
# selectedrows[['_id', '_source.body_analysed']].to_csv(r"C:\Users\k1767582\PycharmProjects\20191025_Epilepsyneurolologyletters\20191101_Epilepsy_dataset\20191101_Epilepsy_clinic_project\Epilepsy_letters_2013_20191001\1000_clinic_letters.csv", header=True, index=False, escapechar='"')
