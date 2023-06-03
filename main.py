from typing import Union
from fastapi import FastAPI
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import ujson
import webbrowser
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load data and models
with open('pub_list_stemmed.json', 'r') as file:
    pub_list_first_stem = ujson.load(file)
with open('pub_indexed_dictionary.json', 'r') as file:
    pub_index = ujson.load(file)
with open('pub_name.json', 'r') as file:
    pub_name = ujson.load(file)
with open('pub_url.json', 'r') as file:
    pub_url = ujson.load(file)
with open('pub_cu_author.json', 'r') as file:
    pub_cu_author = ujson.load(file)
with open('pub_date.json', 'r') as file:
    pub_date = ujson.load(file)

# Initialize NLTK components
stemmer = PorterStemmer()
stop_words = stopwords.words('english')
tfidf = TfidfVectorizer()

# Function to perform publication search
# def pub_qp_data(query):
#     abc = {}
#     query = query.lower().split()
#     pointer = []
#     # if len(query) < 2:
#     #         return "Please enter at least 2 words .. "
#     for token in query:
#         if len(token) <= 3:
#             return "Error!!!", "Please enter more than 4 characters."
#         stem_temp = ""
#         stem_word_file = []
#         temp_file = []
#         word_list = word_tokenize(token)
#         for x in word_list:
#             if x not in stop_words:
#                 stem_temp += stemmer.stem(x) + " "
#         stem_word_file.append(stem_temp)
#         if pub_index.get(stem_word_file[0].strip()):
#             pointer = pub_index.get(stem_word_file[0].strip())
#             # print("pointer", pointer)
#         else:
#             if len(query) == 1:
#                 pointer = []

#         if len(pointer) == 0:
#             abc = {}
#         else:
#             for j in pointer:
#                 temp_file.append(pub_list_first_stem[j])
#             temp_file = tfidf.fit_transform(temp_file)
#             cosine_output = cosine_similarity(
#                 temp_file, tfidf.transform(stem_word_file))

#             if pub_index.get(stem_word_file[0].strip()):
#                 for j in pointer:
#                     abc[j] = cosine_output[pointer.index(j)]

#     aa = 0
#     rank_sorting = sorted(abc.items(), key=lambda z: z[1], reverse=True)
#     print("rank_sorting", rank_sorting)
#     # for a in rank_sorting:

#     #     outputData.insert(tk.INSERT, "Rank: ")
#     #     outputData.insert(tk.INSERT, "{:.2f}".format(a[1][0]))
#     #     outputData.insert(tk.INSERT, "\n")
#     #     outputData.insert(tk.INSERT, 'Title: ' + pub_name[a[0]] + "\n")
#     #     outputData.insert(tk.INSERT, 'URL: ' + pub_url[a[0]] + "\n", 'link')
#     #     outputData.insert(tk.INSERT, 'Date: ' + pub_date[a[0]] + "\n")
#     #     outputData.insert(tk.INSERT, 'Cov_Uni_Author: ' + pub_cu_author[a[0]] + "\n")
#     #     outputData.insert(tk.INSERT, "\n")
#     #     aa += 1

#     if aa == 0:
#         return "Error!!!", "No results found. Please try again."
#     return rank_sorting

count = 1
# Function to perform publication search


def pub_qp_data(query):
    abc = {}
    query = query.lower().split()
    pointer = []
    match_word = []
    for token in query:
        temp_file = []
        set2 = set()
        stem_word_file = []
        word_list = word_tokenize(token)
        stem_temp = ""
        for x in word_list:
            if x not in stop_words:
                stem_temp += stemmer.stem(x) + " "
        stem_word_file.append(stem_temp)
        if pub_index.get(stem_word_file[0].strip()):
            set1 = set(pub_index.get(stem_word_file[0].strip()))
            pointer.extend(list(set1))

            if match_word == []:
                match_word = list(
                    {z for z in pointer if z in set2 or (set2.add(z) or False)})
            else:
                match_word.extend(list(set1))
                match_word = list(
                    {z for z in match_word if z in set2 or (set2.add(z) or False)})
        else:
            pointer = []

    if len(query) > 1:
        match_word = {z for z in match_word if z in set2 or (
            set2.add(z) or False)}

        if len(match_word) == 0:
            abc = {}
        else:
            for j in list(match_word):
                temp_file.append(pub_list_first_stem[j])
            temp_file = tfidf.fit_transform(temp_file)
            cosine_output = cosine_similarity(
                temp_file, tfidf.transform(stem_word_file))

            for j in list(match_word):
                abc[j] = cosine_output[list(match_word).index(j)]
    else:
        if len(pointer) == 0:
            abc = {}
        else:
            for j in pointer:
                temp_file.append(pub_list_first_stem[j])
            temp_file = tfidf.fit_transform(temp_file)
            cosine_output = cosine_similarity(
                temp_file, tfidf.transform(stem_word_file))

            for j in pointer:
                abc[j] = cosine_output[pointer.index(j)]
    d = []
    aa = 0
    rank_sorting = sorted(abc.items(), key=lambda z: z[1], reverse=True)
    for a in rank_sorting:
        data = {}
        data['title'] = pub_name[a[0]]
        data['URL'] = pub_url[a[0]]
        data['Date'] = pub_date[a[0]]
        data['Cov_Uni_Author'] = pub_cu_author[a[0]]
        d.append(data)
        aa += 1
    if aa == 0:
        return "Error!!!", "No results found. Please try again."
    print("count ", aa)
    return d


app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    # Add the origins that are allowed to access the API
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Search engine"}


@app.get("/search/{query}")
def read_item(query):
    result = pub_qp_data(query)
    return {"query": result}


# to start
# uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
