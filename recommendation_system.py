import json
import tkinter as tk
from tkinter import messagebox

def convert_vote_count(vote_count):
    if vote_count.endswith('K'):
        count = float(vote_count.replace('K', '')) * 1000
        return int(count)
    elif vote_count.endswith('M'):
        count = float(vote_count.replace('M', '')) * 1000000
        return int(count)
    else:
        return int(vote_count.replace('.', '').replace(',', ''))

def load_data_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON format.")
        return None

def save_data_to_file(data, file_name):
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        messagebox.showinfo("Success", "Data saved successfully.")
    except:
        messagebox.showerror("Error", "Failed to save data.")

def get_user_preferences():
    def submit_preferences():
        preferred_writers = writers_entry.get()
        preferred_director = director_entry.get()
        preferred_year = year_entry.get()
        preferred_language = language_entry.get()
        preferences_window.destroy()
        handle_user_preferences(preferred_writers, preferred_director, preferred_year, preferred_language)

    preferences_window = tk.Tk()
    preferences_window.title("User Preferences")
    tk.Label(preferences_window, text="Enter your preferred Writers:").pack()
    writers_entry = tk.Entry(preferences_window)
    writers_entry.pack()
    tk.Label(preferences_window, text="Enter your preferred Director:").pack()
    director_entry = tk.Entry(preferences_window)
    director_entry.pack()
    tk.Label(preferences_window, text="Enter your preferred Year:").pack()
    year_entry = tk.Entry(preferences_window)
    year_entry.pack()
    tk.Label(preferences_window, text="Enter your preferred Language:").pack()
    language_entry = tk.Entry(preferences_window)
    language_entry.pack()
    submit_button = tk.Button(preferences_window, text="Submit", command=submit_preferences)
    submit_button.pack()
    preferences_window.mainloop()

def handle_user_preferences(preferred_writers, preferred_director, preferred_year, preferred_language):
    filtered_movies = filter_movies(preferred_writers, preferred_director, preferred_year, preferred_language, writers_agent, director_agent, year_agent, language_agent)
    if filtered_movies:
        rankings = [movie['ranking'] for movie in filtered_movies]
        unique_rankings = list(set(rankings))
        recommendations = [movie for movie in filtered_movies if movie['ranking'] in unique_rankings]
        sorted_recommendations = recommend_movies(recommendations)
        display_recommendations(sorted_recommendations)
        sorted_recommendations = collect_feedback(sorted_recommendations)
        data['imdb_movies'] = movies
        save_data_to_file(data, 'imdb_data.json')
    else:
        messagebox.showinfo("No Movies", "No movie data available.")

def filter_movies(preferred_writers, preferred_director, preferred_year, preferred_language, writers_agent, director_agent, year_agent, language_agent):
    filtered_movies = []
    for writer in preferred_writers.split(','):
        if writer.strip() in writers_agent:
            filtered_movies.extend(writers_agent[writer.strip()])
    for director in preferred_director.split(','):
        if director.strip() in director_agent:
            filtered_movies.extend(director_agent[director.strip()])
    for year in preferred_year.split(','):
        if year.strip() in year_agent:
            filtered_movies.extend(year_agent[year.strip()])
    for language in preferred_language.split(','):
        if language.strip() in language_agent:
            filtered_movies.extend(language_agent[language.strip()])
    return filtered_movies

def recommend_movies(filtered_movies):
    sorted_movies = sorted(filtered_movies, key=lambda x: (x['ranking'], convert_vote_count(x['vote_count']), int(x['gross_worldwide'].replace('$', '').replace(',', ''))), reverse=True)
    return sorted_movies

def display_recommendations(recommendations):
    num_recommendations = 10
    messagebox.showinfo("Movie Recommendations", "\n".join([f"{i+1}. {movie['movie_name']} ({movie['year']}) - Rating: {movie['rating']}, Vote Count: {movie['vote_count']}, Gross Worldwide: {movie['gross_worldwide']}" for i, movie in enumerate(recommendations[:num_recommendations])]))

def collect_feedback(sorted_recommendations):
    user_feedback = messagebox.askquestion("Feedback", "Did you find the recommendations helpful?")
    if user_feedback.lower() == "yes":
        for movie in sorted_recommendations:
            movie['feedback_count'] = movie.get('feedback_count', 0) + 1
    return sorted_recommendations

# Load movie data from file
data = load_data_from_file('imdb_data.json')

if data:
    # Access the movie data
    movies = data.get('imdb_movies', [])
    # Access the timestamp
    timestamp = data.get('timestamp')
    messagebox.showinfo("Timestamp", f"Timestamp: {timestamp}")

    # Initialize agents
    writers_agent = {}
    director_agent = {}
    year_agent = {}
    language_agent = {}

    for movie in movies:
        # Director Agent Initialization
        directors = movie['director']
        for director in directors:
            if director not in director_agent:
                director_agent[director] = []
            director_agent[director].append(movie)

        # Year Agent Initialization
        year = movie['year']
        if year not in year_agent:
            year_agent[year] = []
        year_agent[year].append(movie)

        # Language Agent Initialization
        languages = movie['language']
        for language in languages:
            if language not in language_agent:
                language_agent[language] = []
            language_agent[language].append(movie)

        # Writers Agent Initialization
        writers = movie['writers']
        for writer in writers:
            if writer not in writers_agent:
                writers_agent[writer] = []
            writers_agent[writer].append(movie)

    # Get user preferences
    get_user_preferences()
else:
    messagebox.showerror("Error", "Failed to load movie data.")

# Start the Tkinter event loop
root.mainloop()
