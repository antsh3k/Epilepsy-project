"""WordCloud generator from text populated CSV"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import warnings
warnings.filterwarnings("ignore")

# Read in CSV file
file_path = input("Enter file path and file name here:") # C:\Users\k1767582\PycharmProjects\20191025_Epilepsyneurolologyletters\20191101_Epilepsy_dataset\20191101_Epilepsy_clinic_project\Epilepsy_letters_2013_20191001\1000_clinic_letters.csv
df = pd.read_csv(file_path, index_col=0)

# Data frame description
print("There are {} observations and {} features in this dataset. \n".format(df.shape[0],df.shape[1]))

# select the relevant text columns of csv document
text = df["_source.body_analysed"].iloc[1]

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(text)

# Display the generated image: lower max_font_size, change the maximum number of word and lighten the background:
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


# To Save the image in the img folder:
# wordcloud.to_file("img/first_review.png")

# To use all documents
text = " ".join(review for review in df["_source.body_analysed"])
print("There are {} words in the combination of all review.".format(len(text)))


# To create a mask
brain_mask = np.array(Image.open(r".\Visualisations\brain_silhouette.png"))  # image of brain mask

# Create a word cloud image
wc = WordCloud(background_color="white", max_words=1000, mask=brain_mask,
               contour_width=3, contour_color='firebrick')  # colors cna be found https://matplotlib.org/2.0.0/examples/color/named_colors.html

# Generate a wordcloud
wc.generate(text)

# show
plt.figure(figsize=[20, 10])
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()

