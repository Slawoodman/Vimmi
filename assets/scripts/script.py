import sqlite3
import pandas as pd
import json


class InvalidJSONError(Exception):
    """Custom exception for invalid JSON errors."""

    pass


def load_json_data(json_file_url):
    try:
        with open(json_file_url, "r") as file:
            return pd.DataFrame(json.load(file)["items"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{json_file_url}' was not found.")
    except json.JSONDecodeError:
        raise InvalidJSONError(
            f"Error: The file '{json_file_url}' is not a valid JSON file."
        )


def connect_to_db():
    conn = sqlite3.connect("movies_db.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movie_groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_rank INTEGER,
            end_rank INTEGER,
            avg_year INTEGER,
            avg_rating REAL,
            best_movie_title TEXT
        )
        """
    )
    return conn, cursor


def calculate_averages(local_list):
    avg_year = round(sum(int(film["year"]) for film in local_list) / len(local_list))
    avg_rating = round(
        sum(float(film["imDbRating"]) for film in local_list) / len(local_list), 2
    )
    best_movie = max(local_list, key=lambda x: x["imDbRating"])["title"]
    return avg_year, avg_rating, best_movie


def insert_movie_group(cursor, start_rank, end_rank, avg_year, avg_rating, best_movie):
    cursor.execute(
        """
        INSERT INTO movie_groups (start_rank, end_rank, avg_year, avg_rating, best_movie_title)
        VALUES (?, ?, ?, ?, ?)
        """,
        (start_rank, end_rank, avg_year, avg_rating, best_movie),
    )


def upload_movies(json_file_url):
    data = load_json_data(json_file_url)
    data["imDbRating"] = pd.to_numeric(data["imDbRating"], errors="coerce")
    data["year"] = pd.to_numeric(data["year"], errors="coerce")

    conn, cursor = connect_to_db()

    for i in range(0, len(data), 10):
        local_list = data[i:i + 10].to_dict("records")
        avg_year, avg_rating, best_movie = calculate_averages(local_list)
        start_rank, end_rank = i + 1, i + len(local_list)
        insert_movie_group(
            cursor, start_rank, end_rank, avg_year, avg_rating, best_movie
        )

    conn.commit()
    conn.close()
    print("Data has been uploaded to the database successfully.")
