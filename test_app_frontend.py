import sys
import warnings
import json
import builtins
import os
import pytest
from io import StringIO

from PyQt5.QtWidgets import QApplication

# Silence deprecation warnings from PyQt5 internals to keep tests clean.
# This suppresses messages like "sipPyTypeDict() is deprecated".
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*sipPyTypeDict.*")

import frontend

# Tests for the PyQt5 GUI (frontend.MovieLibraryGUI).
# These tests use a global `QApplication` fixture (`qt_app`) and create a
# fresh `MovieLibraryGUI` instance for each test through the `gui` fixture.
# The `gui` fixture stubs `save_movies` to avoid writing to disk during
# test execution; the `test_save_movies_writes_file` explicitly uses a
# temporary directory and the real save implementation.


@pytest.fixture(scope="session")
def qt_app():
    """Ensure a single QApplication exists for the test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


@pytest.fixture
def gui(qt_app, monkeypatch):
    """Create a `MovieLibraryGUI` instance and stub out disk writes.

    The returned widget is a real instance, but disk writes are disabled by
    monkeypatching `save_movies` so the tests don't modify the repository's
    `movies.json`. Each test receives a fresh `gui` instance and the
    fixture cleans it up afterwards.
    """
    # Prevent the GUI from writing to disk during most tests
    monkeypatch.setattr(frontend.MovieLibraryGUI, 'save_movies', lambda self: None)
    g = frontend.MovieLibraryGUI()
    yield g
    # Clean up widget to avoid resource leaks
    g.close()


def test_load_movies_handles_missing_file(qt_app, monkeypatch, tmp_path):
    """If `movies.json` is missing, `load_movies()` should return an empty
    list.

    This test uses a temporary working directory (tmp_path) to ensure no
    `movies.json` exists, and constructs a GUI object (with QApplication
    available) to call `load_movies()` safely.
    """
    # Construct the GUI with a QApplication present and test load behavior
    monkeypatch.chdir(tmp_path)
    g = frontend.MovieLibraryGUI()
    assert g.load_movies() == []


def test_display_all_movies_updates_table(gui):
    """`display_all_movies()` must fill the table rows with the movie data
    present in `gui.movies` and make cell values accessible via
    `QTableWidgetItem.text()`.
    """
    gui.movies = [
        {'name': 'A', 'date': '2000', 'director': 'X', 'actor': 'Y', 'genre': 'Z'}
    ]
    gui.display_all_movies()

    assert gui.movies_table.rowCount() == 1
    assert gui.movies_table.item(0, 0).text() == 'A'
    assert gui.movies_table.item(0, 1).text() == '2000'
    assert gui.movies_table.item(0, 2).text() == 'X'
    assert gui.movies_table.item(0, 3).text() == 'Y'
    assert gui.movies_table.item(0, 4).text() == 'Z'


def test_filter_movies_shows_no_results_and_back(gui):
    """When filters match no movies, show the 'no results' label and hide
    the table; then `display_all_movies()` should restore the table view.

    Note: we call `QApplication.processEvents()` after mutating UI state so
    that widget visibility updates are processed by the event loop.
    """
    gui.movies = [
        {'name': 'Alpha', 'date': '2001', 'director': '', 'actor': '', 'genre': ''}
    ]
    # Show the window so the visibility of child widgets is meaningful
    gui.show()
    QApplication.processEvents()
    # set a filter that doesn't match
    gui.name_input.setText('nonexistent')
    gui.filter_movies()
    # Process events to ensure widget visibility changes take effect
    QApplication.processEvents()

    assert gui.no_results_label.isVisible()
    assert gui.back_button.isVisible()
    assert not gui.movies_table.isVisible()

    # calling display_all_movies should return UI to full list view
    gui.display_all_movies()
    QApplication.processEvents()
    QApplication.processEvents()
    assert gui.movies_table.isVisible()
    assert not gui.no_results_label.isVisible()


def test_delete_movie_removes_entry(gui):
    """`delete_movie(index)` should remove the movie at the given index and
    update the in-memory list as well as the displayed table rows.
    """
    gui.movies = [
        {'name': 'One', 'date': '', 'director': '', 'actor': '', 'genre': ''},
        {'name': 'Two', 'date': '', 'director': '', 'actor': '', 'genre': ''},
    ]
    gui.display_all_movies()
    gui.delete_movie(0)

    assert len(gui.movies) == 1
    assert gui.movies[0]['name'] == 'Two'


def test_save_movies_writes_file(tmp_path, monkeypatch):
    """`save_movies()` should persist `gui.movies` to a file named
    `movies.json` in the current working directory; this test changes the
    working directory to a temporary path (tmp_path) to avoid touching the
    repository's files.
    """
    # Change working directory to a temporary path so we do not touch repo files
    monkeypatch.chdir(tmp_path)

    g = frontend.MovieLibraryGUI()
    g.movies = [{'name': 'Saved', 'date': '2025', 'director': 'D', 'actor': 'A', 'genre': 'G'}]
    # Use the real save implementation for this test
    frontend.MovieLibraryGUI.save_movies(g)

    # Ensure the file was created and contains the expected JSON
    path = tmp_path / 'movies.json'
    assert path.exists()
    data = json.loads(path.read_text())
    assert isinstance(data, list)
    assert data[0]['name'] == 'Saved'
