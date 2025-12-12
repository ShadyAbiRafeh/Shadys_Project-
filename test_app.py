import json
import builtins
import pytest

import backend


@pytest.fixture
def client():
    backend.save_movies = lambda: None  # disable actual file writes during tests
    app = backend.app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page_contains_title(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Movie Library" in res.data


def test_search_movies_returns_json_filtered():
    # search for a movie that exists in movies.json
    with backend.app.test_request_context():
        resp = backend.app.test_client().get('/search', query_string={'name': 'The Matrix'})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert isinstance(data, list)
        assert any('The Matrix' == m['name'] for m in data)


def test_web_search_no_results_shows_message(client):
    res = client.get('/websearch', query_string={'name': 'nonexistentmovie'})
    assert res.status_code == 200
    assert b"No movies found matching the criteria." in res.data


def test_add_movie_appends_movie(client):
    # make sure movies list is isolated for test
    original = list(backend.movies)
    backend.movies.clear()

    res = client.post('/add', data={
        'name': 'Unit Test Movie',
        'date': '2025',
        'director': 'Tester',
        'actor': 'Test Actor',
        'genre': 'Test'
    })

    # add route redirects to home
    assert res.status_code in (302, 301)
    assert any(m['name'] == 'Unit Test Movie' for m in backend.movies)

    # restore original list
    backend.movies[:] = original


def test_delete_movie_removes_entry(client):
    # setup movies list with known entries
    original = list(backend.movies)
    backend.movies[:] = [{'name': 'To Delete', 'date': '', 'director': '', 'actor': '', 'genre': ''},]

    res = client.post('/delete/0')
    assert res.status_code in (302, 301)
    assert all(m['name'] != 'To Delete' for m in backend.movies)

    # restore original list
    backend.movies[:] = original


def test_load_movies_handles_missing_file(monkeypatch):
    # patch builtins.open to raise FileNotFoundError
    def fake_open(*args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr(builtins, 'open', fake_open)
    assert backend.load_movies() == []
