from tkinter import *
from tkinter import messagebox
import numpy as np
import pandas as pd
def search():
    # read all csv files
    links_df = pd.read_csv('data/links.csv')
    movies_df = pd.read_csv('data/movies.csv')
    ratings_df = pd.read_csv('data/ratings.csv')
    tags_df = pd.read_csv('data/tags.csv')
    # dataframe
    df = movies_df.merge(ratings_df, on='movieId')
    user_data = movie_entry.get()
    
    recommended_movies = []
    # Find the movie in the database, and sort it by rating
    try:
        movie_db = df[df['title'] == user_data].sort_values(by='rating', ascending=False)
    except NameError:
        print(NameError)
    else:
        # Get the first 5 users who liked this movie

        for user in movie_db.iloc[:5]['userId'].values:
            
            # Get the rated movies for this user
            rated_movies = df[df['userId'] == user]
            
            # Get the five biggest rated movie by this user
            rated_movies = rated_movies[rated_movies['title'] != user_data]\
                            .sort_values(by='rating', ascending=False)\
                            .iloc[:5]

            # Add these to the recommendations
            recommended_movies.extend(list(rated_movies['title'].values))
            
        recommended_movies = np.unique(recommended_movies)
            
        gmovie_genres = df[df['title'] == user_data].iloc[0]['genres'].split('|')
        scores = {}  # {title: score ...}

        for movie in recommended_movies:
            movied = df[df['title'] == movie].iloc[0]
            movie_genres = movied['genres'].split('|')
            score = 0
        # How many gmovie_genre can be found in movie_genres?
            for gmovie_genre in gmovie_genres:
                if gmovie_genre in movie_genres:
                    score += 1
            
            scores[movie] = score
            
        # Sort them on score and reverse it, because the bigger the score the better 
        recommended_movies = sorted(scores, key=lambda x: scores[x])[::-1]   # Sorts in the reverse order...

        recommended_movies='\n'.join(recommended_movies)
        messagebox.showinfo(title=' Recommended Movies', message=f'{recommended_movies}')

# GUI ----------------------------------------------------------
window = Tk()
window.title("Movie Recommender")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="Netflix-Free-PNG.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
# labels
movie_label = Label(text="Movie Name: ")
movie_label.grid(row=1, column=0)


# Entry
movie_entry = Entry(width=30)
movie_entry.focus()
movie_entry.grid(row=1, column=1)

# Button
search_button = Button(text="Search", command=search)
search_button.config(width=10, padx=15)
search_button.grid(row=1, column=2, columnspan=3)

window.mainloop()