from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import json

app = Flask(__name__)

# Load movies from JSON file
def load_movies():
    try:
        with open('movies.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

movies = load_movies()

def save_movies():
    with open('movies.json', 'w') as f:
        json.dump(movies, f, indent=4)

@app.route('/', methods=['GET'])
def home():
    # Display all movies initially
    results_html = """
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th>Name</th>
                <th>Year</th>
                <th>Director</th>
                <th>Actors</th>
                <th>Genre</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
    """
    for i, movie in enumerate(movies):
        results_html += f"""
            <tr>
                <td>{movie['name']}</td>
                <td>{movie['date']}</td>
                <td>{movie['director']}</td>
                <td>{movie['actor']}</td>
                <td>{movie['genre']}</td>
                <td>
                    <form action="/delete/{i}" method="post" style="display:inline;">
                        <button type="submit">Delete</button>
                    </form>
                </td>
            </tr>
        """
    results_html += """
        </tbody>
    </table>
    """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Movie Library</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f0f0f0;
                color: #333;
            }}
            h1 {{
                color: #2E86C1;
                font-size: 2.5em;
                margin-bottom: 30px;
                text-align: center;
                font-weight: bold;
            }}
            h2 {{
                color: #34495E;
                font-size: 1.5em;
                margin-top: 30px;
                margin-bottom: 15px;
                font-weight: bold;
            }}
            form {{
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .form-group {{
                margin-bottom: 15px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #34495E;
            }}
            input {{
                width: 100%;
                padding: 10px;
                border: 1px solid #BDC3C7;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }}
            input:focus {{
                outline: none;
                border-color: #3498DB;
                box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
            }}
            button {{
                background-color: #3498DB;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                margin-right: 10px;
                margin-top: 10px;
            }}
            button:hover {{
                background-color: #2980B9;
            }}
            .add-button {{
                background-color: #27AE60;
            }}
            .add-button:hover {{
                background-color: #229954;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background-color: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            th {{
                background-color: #34495E;
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: bold;
                font-size: 14px;
            }}
            td {{
                padding: 12px 15px;
                border-bottom: 1px solid #ddd;
            }}
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            tr:hover {{
                background-color: #e9ecef;
            }}
            .delete-button {{
                background-color: #E74C3C;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 3px;
                cursor: pointer;
                font-size: 12px;
                font-weight: bold;
            }}
            .delete-button:hover {{
                background-color: #C0392B;
            }}
        </style>
    </head>
    <body>
        <h1>Movie Library</h1>
        <form action="/add" method="post">
            <div class="form-group">
                <label for="name">Movie Name:</label>
                <input type="text" id="name" name="name" placeholder="Movie Name" required>
            </div>
            <div class="form-group">
                <label for="date">Release Date:</label>
                <input type="text" id="date" name="date" placeholder="Release Date">
            </div>
            <div class="form-group">
                <label for="director">Director:</label>
                <input type="text" id="director" name="director" placeholder="Director">
            </div>
            <div class="form-group">
                <label for="actor">Actor:</label>
                <input type="text" id="actor" name="actor" placeholder="Actor">
            </div>
            <div class="form-group">
                <label for="genre">Genre:</label>
                <input type="text" id="genre" name="genre" placeholder="Genre">
            </div>
            <button type="submit" class="add-button">Add Movie</button>
        </form>
        <form action="/websearch" method="get">
            <div class="form-group">
                <label for="search-name">Movie Name:</label>
                <input type="text" id="search-name" name="name" placeholder="Movie Name">
            </div>
            <div class="form-group">
                <label for="search-date">Release Date:</label>
                <input type="text" id="search-date" name="date" placeholder="Release Date">
            </div>
            <div class="form-group">
                <label for="search-director">Director:</label>
                <input type="text" id="search-director" name="director" placeholder="Director">
            </div>
            <div class="form-group">
                <label for="search-actor">Actor:</label>
                <input type="text" id="search-actor" name="actor" placeholder="Actor">
            </div>
            <div class="form-group">
                <label for="search-genre">Genre:</label>
                <input type="text" id="search-genre" name="genre" placeholder="Genre">
            </div>
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
        results_html = """
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Year</th>
                    <th>Director</th>
                    <th>Actors</th>
                    <th>Genre</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
        """
        for i, movie in enumerate(results):
            results_html += f"""
                <tr>
                    <td>{movie['name']}</td>
                    <td>{movie['date']}</td>
                    <td>{movie['director']}</td>
                    <td>{movie['actor']}</td>
                    <td>{movie['genre']}</td>
                    <td>
                        <form action="/delete/{i}" method="post" style="display:inline;">
                            <button type="submit">Delete</button>
                        </form>
                    </td>
                </tr>
            """
        results_html += """
            </tbody>
        </table>
        """
    else:
        results_html = "<p>No movies found matching the criteria.</p>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Your Movie Library</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f0f0f0;
                color: #333;
            }}
            h1 {{
                color: #2E86C1;
                font-size: 2.5em;
                margin-bottom: 30px;
                text-align: center;
                font-weight: bold;
            }}
            h2 {{
                color: #34495E;
                font-size: 1.5em;
                margin-top: 30px;
                margin-bottom: 15px;
                font-weight: bold;
            }}
            form {{
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .form-group {{
                margin-bottom: 15px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #34495E;
            }}
            input {{
                width: 100%;
                padding: 10px;
                border: 1px solid #BDC3C7;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }}
            input:focus {{
                outline: none;
                border-color: #3498DB;
                box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
            }}
            button {{
                background-color: #3498DB;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                margin-right: 10px;
                margin-top: 10px;
            }}
            button:hover {{
                background-color: #2980B9;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background-color: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            th {{
                background-color: #34495E;
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: bold;
                font-size: 14px;
            }}
            td {{
                padding: 12px 15px;
                border-bottom: 1px solid #ddd;
            }}
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            tr:hover {{
                background-color: #e9ecef;
            }}
            .delete-button {{
                background-color: #E74C3C;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 3px;
                cursor: pointer;
                font-size: 12px;
                font-weight: bold;
            }}
            .delete-button:hover {{
                background-color: #C0392B;
            }}
            .back-link {{
                display: inline-block;
                background-color: #E67E22;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 4px;
                font-weight: bold;
                margin-top: 20px;
            }}
            .back-link:hover {{
                background-color: #D35400;
            }}
            .no-results {{
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                color: #E74C3C;
                font-weight: bold;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Your Movie Library</h1>
        <form action="/websearch" method="get">
            <div class="form-group">
                <label for="search-name">Movie Name:</label>
                <input type="text" id="search-name" name="name" placeholder="Movie Name" value="{request.args.get('name', '')}">
            </div>
            <div class="form-group">
                <label for="search-date">Release Date:</label>
                <input type="text" id="search-date" name="date" placeholder="Release Date" value="{request.args.get('date', '')}">
            </div>
            <div class="form-group">
                <label for="search-director">Director:</label>
                <input type="text" id="search-director" name="director" placeholder="Director" value="{request.args.get('director', '')}">
            </div>
            <div class="form-group">
                <label for="search-actor">Actor:</label>
                <input type="text" id="search-actor" name="actor" placeholder="Actor" value="{request.args.get('actor', '')}">
            </div>
            <div class="form-group">
                <label for="search-genre">Genre:</label>
                <input type="text" id="search-genre" name="genre" placeholder="Genre" value="{request.args.get('genre', '')}">
            </div>
            <button type="submit">Filter</button>
        </form>
        <h2>Results:</h2>
        {results_html}
        <a href="/" class="back-link">Back to Home</a>
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

@app.route('/add', methods=['POST'])
def add_movie():
    name = request.form.get('name', '').strip()
    date = request.form.get('date', '').strip()
    director = request.form.get('director', '').strip()
    actor = request.form.get('actor', '').strip()
    genre = request.form.get('genre', '').strip()

    if name:
        global movies
        movies.append({
            'name': name,
            'date': date,
            'director': director,
            'actor': actor,
            'genre': genre
        })
        save_movies()
    return redirect(url_for('home'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_movie(index):
    global movies
    if 0 <= index < len(movies):
        del movies[index]
        save_movies()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
