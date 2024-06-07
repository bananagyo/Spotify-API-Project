import base64
import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID: str = os.getenv("CLIENT_ID")
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token: str):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    return json_result[0]


def get_artist_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    albums = json_result["items"]
    album_ids = [album["id"] for album in albums]

    return album_ids


def get_album_songs(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    songs = json_result["items"]
    song_names = [song["id"] for song in songs]

    return song_names


def get_all_songs_by_artist(token, artist_id) -> list:
    return [
        song
        for album_id in get_artist_albums(token, artist_id)
        for song in get_album_songs(token, album_id)
    ]


def main():
    token = get_token()

    with open("artists.csv") as f:
        all_songs = []
        for artist in f:
            artist_id = search_for_artist(token, artist.strip())["id"]
            for song in get_all_songs_by_artist(token, artist_id):
                all_songs.append(song)
            print(f"{artist.strip()} completed")
        df = pd.DataFrame(all_songs)
        df.to_csv("songs.csv", index=False)


if __name__ == "__main__":
    main()
