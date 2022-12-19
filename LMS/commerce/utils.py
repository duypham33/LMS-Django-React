
# Functions support course recommendations
import pandas as pd
import numpy as np
import neattext.functions as nfx

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel 
from bs4 import BeautifulSoup # parse HTML
import urllib.request


def readdata():
    df = pd.read_csv('static/assets//udemy_course_data.csv')
    return df



def getcleantitle(df):
    df['Clean_title'] = df['course_title'].apply(lambda x: x.lower())
    df['Clean_title'] = df['Clean_title'].apply(nfx.remove_stopwords)
    df['Clean_title'] = df['Clean_title'].apply(nfx.remove_special_characters)

    return df





def getcosinemat(df):
    countvect = CountVectorizer()
    cvmat = countvect.fit_transform(df['Clean_title'])
    return cvmat

# getting the title which doesn't contain stopwords and all which we removed with the help of nfx


def cosinesimmat(cv_mat):
    return cosine_similarity(cv_mat)


# this is the main recommendation logic for a particular title which is choosen


def recommend_course(df, title, cosine_mat, numrec):
    course_index = pd.Series(
        df.index, index=df['Clean_title']).drop_duplicates()

    index = course_index[title]
    scores = list(enumerate(cosine_mat[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    selected_course_index = [i[0] for i in sorted_scores[1:]]
    selected_course_score = [i[1] for i in sorted_scores[1:]]
    rec_df = df.iloc[selected_course_index]
    rec_df['Similarity_Score'] = selected_course_score

    final_recommended_courses = rec_df[[
        'course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']]

    return final_recommended_courses.head(numrec)


def searchterm(term, df):
    result_df = df[df['Clean_title'].str.contains(term)]
    top = result_df.sort_values(by='num_subscribers', ascending=False).head(24)
    return top


# extract features from the recommended dataframe

def extractfeatures(recdf):
    course_url = list(recdf['url'])
    course_title = list(recdf['course_title'])

    return course_url, course_title


def words(titlename):
  delimeters = [' ', '/', '-', ',', '!', '@', '#', '$', '*', '(', ')', '[', ']', '_']
  results = []
  word = []
  for c in titlename:
    if c in delimeters:
      if len(word) > 0:
        results.append(('').join(word))
        word = []
    else:
      word.append(c)
  
  if len(word) > 0:
    results.append(('').join(word))
  return list(results)


def helper(df, titlename, start):
    try:
        titlename = titlename.lower()
        cvmat = getcosinemat(df)

        num_rec = 24
        cosine_mat = cosinesimmat(cvmat)

        recdf = recommend_course(df, titlename,
                                  cosine_mat, num_rec)

        course_url, course_title = extractfeatures(recdf)

        # print(len(extractimages(course_url[1])))
        order = [i for i in range(start, start + len(course_url))]
        coursemap = dict(zip(course_title, zip(course_url, order)))

        if len(coursemap) != 0:
            return coursemap

        else:
            return {}
    except:

        resultdf = searchterm(titlename, df)
        if resultdf.shape[0] > 24:
            resultdf = resultdf.head(24)
            course_url, course_title = extractfeatures(
                resultdf)
            #coursemap = dict(zip(course_title, course_url))
            order = [i for i in range(start, start + len(course_url))]
            coursemap = dict(zip(course_title, zip(course_url, order)))
            if len(coursemap) != 0:
                return coursemap
            else:
                return {}

        else:
            course_url, course_title = extractfeatures(
                resultdf)
            #coursemap = dict(zip(course_title, course_url))
            order = [i for i in range(start, start + len(course_url))]
            coursemap = dict(zip(course_title, zip(course_url, order)))
            if len(coursemap) != 0:
                return coursemap
            else:
                return {}


def helper2(df, titlename, coursemap):
  start = len(coursemap)
  remain = 24 - start
  if remain <= 0:
    return coursemap
  
  courseset = set(coursemap.items())
  ws = words(titlename)
  for w in ws:
    cs = set(helper(df, w, start).items())
    courseset.update(cs)
    if len(courseset) >= 24:
      break
    
    start = len(courseset)
  
  return list(sorted(courseset, key = lambda x: x[1][1]))



def search(df, titlename):
  coursemap = helper(df, titlename, 0)
  return helper2(df, titlename, coursemap)



def get_course_img(url):
    soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    return soup.find('span', {"class": 'intro-asset--img-aspect--3fbKk'}).find("img").attrs.get('src')