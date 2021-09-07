import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
data = pd.read_csv("Train.csv")
test = pd.read_csv("Test.csv")

cv = CountVectorizer()
X_train_tfidf = cv.fit_transform(data["Ingrediants"])
X_test_tfidf = cv.transform(test["Ingrediants"])
value = X_train_tfidf.toarray()
# print(value[0])
test_value = X_test_tfidf.toarray()
# print(X_test_tfidf.toarray())
max = 0
for i in range(len(value)):
    score = cosine_similarity((value[i],test_value[0]))
    # print(data["Receipe Name"].iloc[i],score[0][1])
    if score[0][1]>max:
       max = score[0][1]
       tag = data["Tag"].iloc[i]

print(tag, max)
