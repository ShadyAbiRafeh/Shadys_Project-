import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget
from PyQt5.QtCore import Qt

class MovieLibraryGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.movies = self.load_movies()
        self.initUI()
        self.display_all_movies()

    def load_movies(self):
        try:
            with open('movies.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def initUI(self):
        self.setWindowTitle('Movie Library')
        self.setGeometry(100, 100, 600, 400)

        # Create layout
        layout = QVBoxLayout()

        # Search fields
        search_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Movie Name')
        search_layout.addWidget(QLabel('Name:'))
        search_layout.addWidget(self.name_input)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText('Release Date')
        search_layout.addWidget(QLabel('Date:'))
        search_layout.addWidget(self.date_input)

        self.director_input = QLineEdit()
        self.director_input.setPlaceholderText('Director')
        search_layout.addWidget(QLabel('Director:'))
        search_layout.addWidget(self.director_input)

        self.actor_input = QLineEdit()
        self.actor_input.setPlaceholderText('Actor')
        search_layout.addWidget(QLabel('Actor:'))
        search_layout.addWidget(self.actor_input)

        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText('Genre')
        search_layout.addWidget(QLabel('Genre:'))
        search_layout.addWidget(self.genre_input)

        # Filter button
        self.filter_button = QPushButton('Filter')
        self.filter_button.clicked.connect(self.filter_movies)
        search_layout.addWidget(self.filter_button)

        layout.addLayout(search_layout)

        # Movies list
        self.movies_list = QListWidget()
        layout.addWidget(QLabel('All Movies:'))
        layout.addWidget(self.movies_list)

        self.setLayout(layout)

    def display_all_movies(self):
        self.movies_list.clear()
        for movie in self.movies:
            item_text = f"{movie['name']} ({movie['date']}) - Directed by {movie['director']} - Actors: {movie['actor']} - Genre: {movie['genre']}"
            self.movies_list.addItem(item_text)

    def filter_movies(self):
        # Get input values
        name = self.name_input.text().strip().lower()
        date = self.date_input.text().strip().lower()
        director = self.director_input.text().strip().lower()
        actor = self.actor_input.text().strip().lower()
        genre = self.genre_input.text().strip().lower()

        # Filter movies based on criteria
        filtered_movies = []
        for movie in self.movies:
            if (name in movie['name'].lower() or not name) and \
               (date in movie['date'].lower() or not date) and \
               (director in movie['director'].lower() or not director) and \
               (actor in movie['actor'].lower() or not actor) and \
               (genre in movie['genre'].lower() or not genre):
                filtered_movies.append(movie)

        # Display filtered results
        self.movies_list.clear()
        if not filtered_movies:
            self.movies_list.addItem('No movies found matching the criteria.')
        else:
            for movie in filtered_movies:
                item_text = f"{movie['name']} ({movie['date']}) - Directed by {movie['director']} - Actors: {movie['actor']} - Genre: {movie['genre']}"
                self.movies_list.addItem(item_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MovieLibraryGUI()
    gui.show()
    sys.exit(app.exec_())
