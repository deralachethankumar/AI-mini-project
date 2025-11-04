import tkinter as tk
from tkinter import ttk, messagebox
import random

# -------------------------------
# Movie Data (small sample dataset)
# -------------------------------
movies = [
    {"title": "Inception", "genre": ["Sci-Fi", "Action"], "rating": 8.8},
    {"title": "The Dark Knight", "genre": ["Action", "Drama"], "rating": 9.0},
    {"title": "Interstellar", "genre": ["Sci-Fi", "Adventure"], "rating": 8.6},
    {"title": "The Shawshank Redemption", "genre": ["Drama"], "rating": 9.3},
    {"title": "Avengers: Endgame", "genre": ["Action", "Fantasy"], "rating": 8.4},
    {"title": "Coco", "genre": ["Animation", "Family"], "rating": 8.4},
    {"title": "Frozen II", "genre": ["Animation", "Adventure"], "rating": 6.8},
    {"title": "Joker", "genre": ["Crime", "Drama"], "rating": 8.5},
    {"title": "Toy Story 4", "genre": ["Animation", "Comedy"], "rating": 7.7},
    {"title": "The Matrix", "genre": ["Action", "Sci-Fi"], "rating": 8.7},
    {"title": "Parasite", "genre": ["Drama", "Thriller"], "rating": 8.6},
    {"title": "Tenet", "genre": ["Action", "Sci-Fi"], "rating": 7.4},
    {"title": "Encanto", "genre": ["Animation", "Musical"], "rating": 7.2},
]

# -------------------------------
# Probabilistic Reasoning
# -------------------------------
# Prior probabilities (user preference likelihoods)
genre_priors = {
    "Action": 0.15,
    "Drama": 0.15,
    "Sci-Fi": 0.15,
    "Adventure": 0.1,
    "Animation": 0.1,
    "Comedy": 0.1,
    "Thriller": 0.05,
    "Fantasy": 0.05,
    "Family": 0.05,
    "Crime": 0.05,
    "Musical": 0.05
}

# Conditional probabilities (based on mood)
conditional_prefs = {
    "Happy": {"Comedy": 0.3, "Animation": 0.3, "Adventure": 0.2, "Drama": 0.1},
    "Sad": {"Drama": 0.4, "Family": 0.3, "Animation": 0.2},
    "Excited": {"Action": 0.4, "Sci-Fi": 0.3, "Adventure": 0.2},
    "Thoughtful": {"Drama": 0.4, "Sci-Fi": 0.3, "Thriller": 0.2},
    "Relaxed": {"Comedy": 0.3, "Fantasy": 0.3, "Animation": 0.2}
}

# -------------------------------
# Probabilistic Recommendation Logic
# -------------------------------
def recommend_movies(selected_genres, mood):
    probs = genre_priors.copy()

    # Update probabilities based on user-selected genres
    for g in selected_genres:
        if g in probs:
            probs[g] *= 2.0  # boost chosen genre probability

    # Incorporate mood conditionals (Bayesian update)
    if mood in conditional_prefs:
        for g, val in conditional_prefs[mood].items():
            probs[g] *= (1 + val)  # weight by mood preference

    # Normalize probabilities
    total = sum(probs.values())
    for g in probs:
        probs[g] /= total

    # Score each movie based on its genre probabilities
    movie_scores = []
    for m in movies:
        score = sum(probs.get(g, 0) for g in m["genre"])
        movie_scores.append((m["title"], score, m["rating"], ", ".join(m["genre"])))

    # Sort by score and rating
    movie_scores.sort(key=lambda x: (x[1], x[2]), reverse=True)
    top = movie_scores[:5]

    return top

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("🎬 Movie Recommendation System (Probabilistic Reasoning)")
root.geometry("700x550")

# Header
tk.Label(root, text="🎥 Movie Recommendation System", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(root, text="Select your preferences below", font=("Arial", 11)).pack(pady=5)

# Genre Selection
genres = list(genre_priors.keys())
genre_vars = {}

frame_genres = tk.LabelFrame(root, text="Select Your Favorite Genres")
frame_genres.pack(padx=10, pady=10, fill="x")

cols = 3
for i, g in enumerate(genres):
    var = tk.BooleanVar()
    chk = tk.Checkbutton(frame_genres, text=g, variable=var)
    chk.grid(row=i // cols, column=i % cols, sticky="w", padx=5, pady=2)
    genre_vars[g] = var

# Mood Dropdown
tk.Label(root, text="Select Your Mood:", font=("Arial", 11)).pack(pady=5)
mood_var = tk.StringVar()
moods = list(conditional_prefs.keys())
mood_dropdown = ttk.Combobox(root, textvariable=mood_var, values=moods, state="readonly")
mood_dropdown.pack(pady=5)
mood_dropdown.set(moods[0])

# Output box
result_box = tk.Text(root, height=15, width=80, bg="#f9f9f9", fg="black", font=("Consolas", 10))
result_box.pack(padx=10, pady=10)

# Recommendation button
def show_recommendations():
    selected = [g for g, v in genre_vars.items() if v.get()]
    mood = mood_var.get()
    if not selected:
        messagebox.showerror("Error", "Please select at least one genre.")
        return

    recs = recommend_movies(selected, mood)
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"Top Movie Recommendations for mood '{mood}'\n")
    result_box.insert(tk.END, "-" * 65 + "\n")
    for title, score, rating, genre_list in recs:
        result_box.insert(tk.END, f"🎬 {title}  |  Genres: {genre_list}  |  Rating: {rating}  |  Score: {score:.3f}\n")

tk.Button(root, text="🎯 Get Recommendations", command=show_recommendations, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

root.mainloop()
