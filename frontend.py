import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

# Simple PyQt5 frontend GUI for the "Your Movie Library" application.
# This file defines a `MovieLibraryGUI` QWidget that provides a visual
# interface for searching, viewing, adding, and deleting movies stored in
# a JSON file on disk (movies.json).

class MovieLibraryGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.movies = self.load_movies()
        self.initUI()
        self.display_all_movies()

    # Instantiate the GUI and initialize state: load movies and build UI.

    def load_movies(self):
        # Load movies from JSON file. If the file is not present, return an
        # empty list to allow the GUI to operate without errors.
        try:
            with open('movies.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def initUI(self):
        self.setWindowTitle('Movie Library')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Create the main vertical layout for the window.
        # Widgets are stacked vertically and grouped into logical sections.
        layout = QVBoxLayout()

        # Top-level title label
        title_label = QLabel('Movie Library')
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E86C1; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Search input fields and controls
        search_layout = QVBoxLayout()

        # Input field for searching by movie name
        name_label = QLabel('Name:')
        name_label.setStyleSheet("font-weight: bold; color: #34495E;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Movie Name')
        self.name_input.setStyleSheet("padding: 5px; border: 1px solid #BDC3C7; border-radius: 3px;")
        search_layout.addWidget(name_label)
        search_layout.addWidget(self.name_input)

        # Input field for searching by release date
        date_label = QLabel('Date:')
        date_label.setStyleSheet("font-weight: bold; color: #34495E;")
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText('Release Date')
        self.date_input.setStyleSheet("padding: 5px; border: 1px solid #BDC3C7; border-radius: 3px;")
        search_layout.addWidget(date_label)
        search_layout.addWidget(self.date_input)

        # Input field for searching by director
        director_label = QLabel('Director:')
        director_label.setStyleSheet("font-weight: bold; color: #34495E;")
        self.director_input = QLineEdit()
        self.director_input.setPlaceholderText('Director')
        self.director_input.setStyleSheet("padding: 5px; border: 1px solid #BDC3C7; border-radius: 3px;")
        search_layout.addWidget(director_label)
        search_layout.addWidget(self.director_input)

        # Input field for searching by actor(s)
        actor_label = QLabel('Actor:')
        actor_label.setStyleSheet("font-weight: bold; color: #34495E;")
        self.actor_input = QLineEdit()
        self.actor_input.setPlaceholderText('Actor')
        self.actor_input.setStyleSheet("padding: 5px; border: 1px solid #BDC3C7; border-radius: 3px;")
        search_layout.addWidget(actor_label)
        search_layout.addWidget(self.actor_input)

        # Input field for searching by genre
        genre_label = QLabel('Genre:')
        genre_label.setStyleSheet("font-weight: bold; color: #34495E;")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText('Genre')
        self.genre_input.setStyleSheet("padding: 5px; border: 1px solid #BDC3C7; border-radius: 3px;")
        search_layout.addWidget(genre_label)
        search_layout.addWidget(self.genre_input)

        # Button to apply the current search/filter values
        self.filter_button = QPushButton('Filter')
        self.filter_button.clicked.connect(self.filter_movies)
        self.filter_button.setStyleSheet("background-color: #3498DB; color: white; padding: 8px; border: none; border-radius: 3px; font-weight: bold;")
        search_layout.addWidget(self.filter_button)

        # Button to open an 'Add Movie' dialog and append a new movie
        self.add_button = QPushButton('Add Movie')
        self.add_button.clicked.connect(self.add_movie)
        self.add_button.setStyleSheet("background-color: #27AE60; color: white; padding: 8px; border: none; border-radius: 3px; font-weight: bold;")
        search_layout.addWidget(self.add_button)

        layout.addLayout(search_layout)

        # Table showing the list of movies. The last column contains a Delete
        # button for each row to remove that movie from the library.
        movies_label = QLabel('All Movies:')
        movies_label.setStyleSheet("font-weight: bold; color: #34495E; margin-top: 10px;")
        layout.addWidget(movies_label)

        self.movies_table = QTableWidget()
        self.movies_table.setColumnCount(6)
        self.movies_table.setHorizontalHeaderLabels(['Name', 'Year', 'Director', 'Actors', 'Genre', 'Actions'])
        self.movies_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.movies_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #BDC3C7;
                background-color: white;
                border: 1px solid #BDC3C7;
            }
            QHeaderView::section {
                background-color: #34495E;
                color: white;
                padding: 8px;
                border: 1px solid #BDC3C7;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        layout.addWidget(self.movies_table)

        # Widgets for when a search yields no results plus a button to go
        # back to the main list (display_all_movies).
        self.no_results_label = QLabel('No movies found matching the criteria.')
        self.no_results_label.setStyleSheet("color: #E74C3C; font-weight: bold; margin-top: 10px;")
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.display_all_movies)
        self.back_button.setStyleSheet("background-color: #E67E22; color: white; padding: 8px; border: none; border-radius: 3px; font-weight: bold;")
        layout.addWidget(self.no_results_label)
        layout.addWidget(self.back_button)

        # Start with the "no results" message hidden.
        self.no_results_label.hide()
        self.back_button.hide()

        self.setLayout(layout)

    def display_all_movies(self):
        # Show the entire `movies` list in the table.
        # Reset UI state so the no-results message is hidden.
        self.movies_table.show()
        self.no_results_label.hide()
        self.back_button.hide()
        self.movies_table.setRowCount(len(self.movies))
        # Fill table rows with movie data and attach Delete buttons that call
        # `delete_movie` with the corresponding row index.
        for row, movie in enumerate(self.movies):
            self.movies_table.setItem(row, 0, QTableWidgetItem(movie['name']))
            self.movies_table.setItem(row, 1, QTableWidgetItem(movie['date']))
            self.movies_table.setItem(row, 2, QTableWidgetItem(movie['director']))
            self.movies_table.setItem(row, 3, QTableWidgetItem(movie['actor']))
            self.movies_table.setItem(row, 4, QTableWidgetItem(movie['genre']))
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(lambda checked, r=row: self.delete_movie(r))
            self.movies_table.setCellWidget(row, 5, delete_button)

    def filter_movies(self):
        # Gather normalized search filter values from UI inputs.
        name = self.name_input.text().strip().lower()
        date = self.date_input.text().strip().lower()
        director = self.director_input.text().strip().lower()
        actor = self.actor_input.text().strip().lower()
        genre = self.genre_input.text().strip().lower()

        # Apply search criteria (case-insensitive) across all movies.
        filtered_movies = []
        for movie in self.movies:
            if (name in movie['name'].lower() or not name) and \
               (date in movie['date'].lower() or not date) and \
               (director in movie['director'].lower() or not director) and \
               (actor in movie['actor'].lower() or not actor) and \
               (genre in movie['genre'].lower() or not genre):
                filtered_movies.append(movie)

        # Update the UI based on whether any movies matched the filter.
        if not filtered_movies:
            self.movies_table.hide()
            self.no_results_label.show()
            self.back_button.show()
        else:
            self.movies_table.show()
            self.no_results_label.hide()
            self.back_button.hide()
            self.movies_table.setRowCount(len(filtered_movies))
            for row, movie in enumerate(filtered_movies):
                self.movies_table.setItem(row, 0, QTableWidgetItem(movie['name']))
                self.movies_table.setItem(row, 1, QTableWidgetItem(movie['date']))
                self.movies_table.setItem(row, 2, QTableWidgetItem(movie['director']))
                self.movies_table.setItem(row, 3, QTableWidgetItem(movie['actor']))
                self.movies_table.setItem(row, 4, QTableWidgetItem(movie['genre']))
                delete_button = QPushButton('Delete')
                delete_button.clicked.connect(lambda checked, r=row: self.delete_movie(r))
                self.movies_table.setCellWidget(row, 5, delete_button)

    def add_movie(self):
        # Open a dialog to collect fields for a new movie, then append it to
        # the in-memory list and persist it when the user accepts.
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
        dialog = QDialog(self)
        dialog.setWindowTitle('Add New Movie')
        layout = QFormLayout()

        name_edit = QLineEdit()
        date_edit = QLineEdit()
        director_edit = QLineEdit()
        actor_edit = QLineEdit()
        genre_edit = QLineEdit()

        layout.addRow('Name:', name_edit)
        layout.addRow('Year:', date_edit)
        layout.addRow('Director:', director_edit)
        layout.addRow('Actors:', actor_edit)
        layout.addRow('Genre:', genre_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            new_movie = {
                'name': name_edit.text().strip(),
                'date': date_edit.text().strip(),
                'director': director_edit.text().strip(),
                'actor': actor_edit.text().strip(),
                'genre': genre_edit.text().strip()
            }
            # Only add a movie if it has a non-empty name field.
            if new_movie['name']:
                self.movies.append(new_movie)
                self.save_movies()
                self.display_all_movies()

    def delete_movie(self, row):
        # Remove a movie safely by its index in the current list and persist
        # the updated movies to disk.
        if 0 <= row < len(self.movies):
            del self.movies[row]
            self.save_movies()
            self.display_all_movies()

    def save_movies(self):
        # Persist the current list of movies to the local `movies.json` file.
        # This overwrites the file with the current in-memory state.
        with open('movies.json', 'w') as f:
            json.dump(self.movies, f, indent=4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MovieLibraryGUI()
    gui.show()
    sys.exit(app.exec_())
