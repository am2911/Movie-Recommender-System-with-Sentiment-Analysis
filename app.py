import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np
#from sklearn.feature_extraction.text import CountVectorizer
#k_zo8eo3nr

def fetch_poster(movie_id):
    try:
        response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(movie_id))
        data=response.json()
        return  "https://image.tmdb.org/t/p/w500/"+ data["poster_path"]
    except :
        pass

def fetch_review1(movie_id):
    response= requests.get('https://imdb-api.com/en/API/Reviews/k_zo8eo3nr/{}'.format(movie_id))
    data=response.json()
    
    try:    
        #print(data["results"][0]["author"])
        #print(data["items"][20]["content"])       
        return data["items"][20]["content"]  ,data["items"][19]["content"] , data["items"][23]["content"] ,data["items"][22]["content"]  
    except:
        pass 

def sel_review(movie):  
    s_m__id=movies[movies["title"]==movie].movie_id.values[0]
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(s_m__id))
    data=response.json()
    imdb_id=data["imdb_id"]
    print(imdb_id)

    selected_movie_review1=[]
    selected_movie_review1.append(fetch_review1(imdb_id))
    result=selected_movie_review1[0]
    return  result

def fetch_overview(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(movie_id))
    data=response.json()
    return  data["overview"]

def fetch_rating(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(movie_id))
    data=response.json()
    print(data["id"])
    return  data["vote_average"]

def fetch_genre(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(movie_id))
    data=response.json()
    return  data["genres"]

def fetch_date(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(movie_id))
    data=response.json()
    return data["release_date"]

def fetch_lang(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(movie_id))
    data=response.json()
    return data["original_language"]

def fetch_status(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(movie_id))
    data=response.json()
    return data["status"]


def recommend(movie):    
    try:
        s_m__id=movies[movies["title"]==movie].movie_id.values[0]
        movie_index=movies[movies["title"]==movie].index[0]
        distances=similarity[movie_index]
        movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1]) [1:6]
    
    except:
        pass
    recommended_movie=[]
    recommended_movie_poster=[]

# get_details=[]
    selected_movie_poster=[]
    selected_movie_rating=[]
    selected_movie_overview=[]

    selected_movie_genres=[]
    selected_movie_date=[]
    selected_movie_lang=[]
    selected_movie_staus=[]
    
    #fetch selected movie poster
    selected_movie_poster.append(fetch_poster(s_m__id))
    selected_movie_rating.append(fetch_rating(s_m__id))
    selected_movie_overview.append(fetch_overview(s_m__id))
    
    selected_movie_genres.append(fetch_genre(s_m__id))
    selected_movie_date.append(fetch_date(s_m__id))
    selected_movie_lang.append(fetch_lang(s_m__id))
    selected_movie_staus.append(fetch_status(s_m__id))
    
    try:
        id=[]                   # recommended movie imdb id
        for i in movie_list:
            movie_id=movies.iloc[i[0]].movie_id
            recommended_movie.append(movies.iloc[i[0]].title)

            response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a5c07beb848695f343d5e9036bd6a4e1&language=en-US'.format(movie_id))
            data=response.json()
            imdb_id=data["imdb_id"]
            id.append(imdb_id)

            # fetch posters from api
            recommended_movie_poster.append( fetch_poster(movie_id))
    except: 
        pass
    return recommended_movie ,recommended_movie_poster,selected_movie_poster,selected_movie_rating, selected_movie_overview, selected_movie_genres,selected_movie_date,selected_movie_lang,selected_movie_staus,id
    
movies_dict=pickle.load(open("movie_dict.pkl","rb"))
movies=pd.DataFrame(movies_dict) 

similarity=pickle.load(open("similarity.pkl","rb"))
                            
                            # Movie Recommeder System
st.markdown("<h1 style='text-align: center; color: white;'>Movie Recommeder System</h1>", unsafe_allow_html=True)

selected_movie_name = st.sidebar.selectbox(
     'Movie You Like the Most !',
    movies["title"].values)

st.write('You selected:', selected_movie_name)

names,posters,sel_poster,sel_rating,overview,genres,release_date,language,status,id= recommend(selected_movie_name)
col1, col2 = st.columns(2)
try:
    with col1:
        st.image(sel_poster)
    with col2:
        st.text(f"TITLE: {selected_movie_name}")
        st.text(" OVERVIEW:") 
        st.caption(overview[0])
        st.text(f"RATING: {sel_rating[0]}⭐")
        a=genres[0]
        s=' '
        for i in a:
            s+=i['name']
            s+=','
        l=len(s)    
        st.text("GENRES:"+s[:l-1])
        #print(genres[0])
        st.text(f" RELEASE DATE: {release_date[0]}")
        st.text(f"LANGUAGE: {language[0]}")
        st.text(f"STATUS: {status[0]}")
except:
    pass
if st.header("More like this") or 1: 
#if st.button('Recommend') or 1:
    names,posters,sel_poster ,sel_rating,overview,genres,release_date,language,status,id= recommend(selected_movie_name)
    
   
    col1, col2, col3,col4,col5 = st.columns(5)
    try:      
        #print(f" {id}")
        link1=("https://www.imdb.com/title/{}/".format(id[0]))
        link2=("https://www.imdb.com/title/{}/".format(id[1]))
        link3=("https://www.imdb.com/title/{}/".format(id[2]))
        link4=("https://www.imdb.com/title/{}/".format(id[3]))
        link5=("https://www.imdb.com/title/{}/".format(id[4]))
        with col1:
            st.image(posters[0])
            st.markdown(f"[{names[0]}]({link1})")    
        with col2:
            st.image(posters[1])
            st.markdown(f"[{names[1]}]({link2})") 
        with col3:
            st.image(posters[2])
            st.markdown(f"[{names[2]}]({link3})") 
        with col4:
            st.image(posters[3])
            st.markdown(f"[{names[3]}]({link4})") 
        with col5:
            st.image(posters[4])
            st.markdown(f"[{names[4]}]({link5})") 
                
                
    except:
        st.markdown("<h6 style='text-align: center; color: red;'>Sorry ! No more recommendations are available for this movie...Please try another one !!</h6>", unsafe_allow_html=True)


                                                # Users Review Part
st.title("Users Review")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Comments")
with col2:
    st.subheader("Review")

# load nlp model and tfidf vectorizer
filename="nlp_model.pkl"
clf=pickle.load(open(filename,"rb"))
vectorizer=pickle.load(open("tranform.pkl","rb"))

try:
    review1=sel_review(selected_movie_name)  
    col1, col2 = st.columns(2)
    reviews_list=[[review1[0]],[review1[1]],[review1[2]],[review1[3]]]    # list of comments   


    # Having no null comments
    res=[]
    for i in reviews_list:
        if i!=['']:
            res+=i
    print(res)

    reviews_status=[]                                 # list of Reviews
    for reviews in reviews_list:
        if reviews!=['']:
            new_list=np.array(list(reviews))
            movie_vector=vectorizer.transform(new_list)
            pred=clf.predict(movie_vector)
            reviews_status.append("Good" if pred else "Bad")
    print(reviews_status)

except:
    pass
    

with col1:
    try:
        st.caption( res[0])
    except:
        pass
 
with col2:
    try:
        st.text(reviews_status[0])
        if reviews_status[0]=="Good":
            st.markdown(""" :smile: """)
        else:
            st.markdown(""" :cry: """)
    except:
        pass

review1=sel_review(selected_movie_name)
col1, col2 = st.columns(2)
with col1:
    try:
        st.caption( res[1])
    except:
        pass
with col2:
    try:
        st.text(reviews_status[1])
        if reviews_status[1]=="Good":
            st.markdown(""" :smile: """)
        else:
            st.markdown(""" :cry: """)
    except:
        pass

review1=sel_review(selected_movie_name)
col1, col2 = st.columns(2)
with col1:
    try:
        st.caption(res[2] )
    except:
        pass
with col2:
    try:
        st.text(reviews_status[2])
        if reviews_status[2]=="Good":
            st.markdown(""" :smile: """)
        else:
            st.markdown(""" :cry: """)
    except:
        pass

review1=sel_review(selected_movie_name)
col1, col2 = st.columns(2)
with col1:
    try:
        st.caption( res[3])
    except:
        pass
with col2:
    try:
        st.text(reviews_status[3])
        if reviews_status[3]=="Good":
            st.markdown(""" :smile: """)
        else:
            st.markdown(""" :cry: """)
    except:
        pass
