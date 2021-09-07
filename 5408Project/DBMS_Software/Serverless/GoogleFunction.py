import math
import re
from collections import Counter
import csv

WORD = re.compile(r"\w+")

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


# ------------------------------------------Program Execution Begins Here----------------------------------------------------------------------------------------------
riceReceipe = "Take a bowl of water and cup of rice Keep it in cooker for 10 minutes White Rice will be ready "
pastaReceipe = "Take a cup of water and pasta Put them in the bowl and boil for 10 minutes Filter the water Add the masala to it and pasta is ready"

vector1 = text_to_vector(riceReceipe)
vector2 = text_to_vector(pastaReceipe)

cosineValue = get_cosine(vector1, vector2)

print("Cosine Similarity between the files is", cosineValue)

if (cosineValue > 0.7):
    print ("Something")


header = ['Input File', 'Existing File', 'Similarity Score']

data = [
    [riceReceipe, pastaReceipe,cosineValue]
]

with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)