# Content-Based-Movie-Recommender-System-with-sentiment-analysis

A Content-Based Recommender System that recommends the top 5  similar  movies that users like the most and analyzes the sentiments on the reviews for that movie.

The details of the movies(title, genre, runtime, rating, poster,reviews, etc) are fetched using IMDB and TMDB API ,
and using the IMDB id of the movie in the API, I did web scraping to get the reviews given by the user in the IMDB site using requests module and performed sentiment analysis on those reviews and displayed the corresponding emoji for the reviews.

Dataset is collected from Kaggle and IMDB. Cosine Similarity is used to find the top 5 similar movies that user like the most.
