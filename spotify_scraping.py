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


def get_artist_top_songs(token, artist_id):
    url = (
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    )
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    print(result)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_all_songs_by_artist(token, artist_id) -> list:
    return [
        song
        for album_id in get_artist_albums(token, artist_id)
        for song in get_album_songs(token, album_id)
    ]


def get_track_features(token, track_id) -> dict:
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result: dict = json.loads(result.content)
    json_result.pop("uri")
    json_result.pop("track_href")
    json_result.pop("analysis_url")

    return json_result


def get_track_analysis(token, track_id) -> dict:
    url = f"https://api.spotify.com/v1/audio-analysis/{track_id}"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result: dict = json.loads(result.content)

    important_data: dict = json_result["track"]

    drop_keys = [
        "duration",
        "loudness",
        "tempo",
        "num_samples",
        "sample_md5",
        "offset_seconds",
        "window_seconds",
        "analysis_sample_rate",
        "analysis_channels",
        "end_of_fade_in",
        "start_of_fade_out",
        "codestring",
        "code_version",
        "echoprintstring",
        "echoprint_version",
        "synchstring",
        "synch_version",
        "rhythmstring",
        "rhythm_version",
    ]

    for key in drop_keys:
        important_data.pop(key)

    return important_data


def main():
    token = get_token()

    # with open("artists.csv") as f:
    #     all_songs = []
    #     for artist in f:
    #         artist_id = search_for_artist(token, artist.strip())["id"]
    #         print(artist_id)
    #         print(get_artist_top_songs(token, artist_id))
    #         # print(f"{artist.strip()} completed")
    #     df = pd.DataFrame(all_songs)
    #     df.to_csv("songs.csv", index=False)

    # artist_name = "Rihanna"
    # artist_id = search_for_artist(token, artist_name)["id"]
    # print(f"{artist_name=}")
    # print(f"{artist_id=}")
    print(f"{get_artist_albums(token, "1Xyo4u8uXC1ZmMpatF05PJ")=}")

    # with open("songs.csv") as f:
    #     output = []
    #     for idx, song in enumerate(f):
    #         track_info = get_track_features(token, song.strip())
    #         track_info.update(get_track_analysis(token, song.strip()))
    #         output.append(track_info)

    #         print(f"{song} completed")

    #         if idx == 10:
    #             break

    #     df = pd.DataFrame(output)
    #     df.to_csv("song_data.csv", index=False)


if __name__ == "__main__":
    main()
