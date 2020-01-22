""" Preprocessing data // Converting Columns in xlsx files from string to datetime format"""

import xlrd
import pandas as pd
import numpy as np
from datetime import datetime
from openpyxl import load_workbook

# Load file
file_location = r"C:\Users\k1767582\Desktop\Rolandic_ep\Rolandic_search_2010_to_25_feb_2019.xlsx"
workbook = pd.ExcelFile(file_location)

# Get sheet names
workbook_sheet_names = workbook.sheet_names
print(workbook_sheet_names)

#parse the tabs
search_date = workbook.parse("search_date")
sheet_2016_17 = workbook.parse("2016-17")
sheet_2017_18 = workbook.parse("2017-18")
sheet_2018_19 = workbook.parse("2018-19")
sheet_2010_2013 = workbook.parse("2010-2013")
sheet_2013_2016 = workbook.parse("2013-2016")


# Select the columns and clean up the column names
sheet_2010_2013.columns = sheet_2010_2013.columns.str.strip().str.lower().str.replace(" ", "-").str.replace('(','').str.replace(')','')
print(sheet_2010_2013.head(0))

sheet_2013_2016.columns = sheet_2013_2016.columns.str.strip().str.lower().str.replace(" ", "-").str.replace('(','').str.replace(')','')
print(sheet_2013_2016.head(0))



# change column format from string to datetime

def datetime (column_name, sheetname):

    new_list= []
    for cell in sheetname[column_name]:
        print(str(cell))
        if str(cell) == "NaT":
            new_list.append("N/A")
        else:
            try:
                new_list.append(pd.to_datetime(cell))
            except:
                new_list.append("N/A")
    return new_list


sheet_2010_2013["client_dob"] = datetime("client_dob", sheet_2010_2013)
sheet_2010_2013["updatetime"] = datetime("updatetime", sheet_2010_2013)

sheet_2013_2016["client_dob"] = datetime("client_dob", sheet_2013_2016)
sheet_2013_2016["updatetime"] = datetime("updatetime", sheet_2013_2016)


print(sheet_2013_2016["updatetime"].head(10))


# Saving the changes to an excel file


writer = pd.ExcelWriter(file_location, engine="openpyxl")
search_date.to_excel(writer, sheet_name = "search_date", index=False)
sheet_2016_17.to_excel(writer, sheet_name = "sheet_2016_17", index=False)
sheet_2017_18.to_excel(writer, sheet_name = "sheet_2017_18", index=False)
sheet_2018_19.to_excel(writer, sheet_name = "sheet_2018_19", index=False)
sheet_2010_2013.to_excel(writer, sheet_name = "sheet_2010_2013", index=False)
sheet_2013_2016.to_excel(writer, sheet_name = "sheet_2013_2016", index=False)


writer.save()
writer.close()
