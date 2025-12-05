from flask import Flask, request, jsonify, render_template_string
import json

app = Flask(__name__)

# Load movies from JSON file
with open('movies.json', 'r') as f:
    movies = json.load(f)

@app.route('/', methods=['GET'])
def home():
    # Display all movies initially
    results_html = "<ul>"
    for movie in movies:
        results_html += f"<li>{movie['name']} ({movie['date']}) - Directed by {movie['director']} - Actors: {movie['actor']} - Genre: {movie['genre']}</li>"
    results_html += "</ul>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Movie Library</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            form {{ margin-bottom: 20px; }}
            input {{ margin: 5px; padding: 5px; }}
            button {{ padding: 5px 10px; }}
            ul {{ list-style-type: none; }}
            li {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>Movie Library</h1>
        <form action="/websearch" method="get">
            <input type="text" name="name" placeholder="Movie Name">
            <input type="text" name="date" placeholder="Release Date">
            <input type="text" name="director" placeholder="Director">
            <input type="text" name="actor" placeholder="Actor">
            <input type="text" name="genre" placeholder="Genre">
            <button type="submit">Filter</button>
        </form>
        <h2>All Movies:</h2>
        {results_html}
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/websearch', methods=['GET'])
def web_search():
    # Get query parameters
    name = request.args.get('name', '').lower()
    date = request.args.get('date', '').lower()
    director = request.args.get('director', '').lower()
    actor = request.args.get('actor', '').lower()
    genre = request.args.get('genre', '').lower()

    # Filter movies based on search criteria
    results = []
    for movie in movies:
        if (name in movie['name'].lower() or not name) and \
           (date in movie['date'].lower() or not date) and \
           (director in movie['director'].lower() or not director) and \
           (actor in movie['actor'].lower() or not actor) and \
           (genre in movie['genre'].lower() or not genre):
            results.append(movie)

    # Build HTML for results
    results_html = ""
    if results:
        results_html = "<ul>"
        for movie in results:
            results_html += f"<li>{movie['name']} ({movie['date']}) - Directed by {movie['director']} - Actors: {movie['actor']} - Genre: {movie['genre']}</li>"
        results_html += "</ul>"
    else:
        results_html = "<p>No movies found matching the criteria.</p>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Movie Library Search Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            form {{ margin-bottom: 20px; }}
            input {{ margin: 5px; padding: 5px; }}
            button {{ padding: 5px 10px; }}
            ul {{ list-style-type: none; }}
            li {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>Movie Library Search Results</h1>
        <form action="/websearch" method="get">
            <input type="text" name="name" placeholder="Movie Name" value="{request.args.get('name', '')}">
            <input type="text" name="date" placeholder="Release Date" value="{request.args.get('date', '')}">
            <input type="text" name="director" placeholder="Director" value="{request.args.get('director', '')}">
            <input type="text" name="actor" placeholder="Actor" value="{request.args.get('actor', '')}">
            <input type="text" name="genre" placeholder="Genre" value="{request.args.get('genre', '')}">
            <button type="submit">Search</button>
        </form>
        <h2>Results:</h2>
        {results_html}
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/search', methods=['GET'])
def search_movies():
    # Get query parameters
    name = request.args.get('name', '').lower()
    date = request.args.get('date', '').lower()
    director = request.args.get('director', '').lower()
    actor = request.args.get('actor', '').lower()
    genre = request.args.get('genre', '').lower()

    # Filter movies based on search criteria
    results = []
    for movie in movies:
        if (name in movie['name'].lower() or not name) and \
           (date in movie['date'].lower() or not date) and \
           (director in movie['director'].lower() or not director) and \
           (actor in movie['actor'].lower() or not actor) and \
           (genre in movie['genre'].lower() or not genre):
            results.append(movie)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
