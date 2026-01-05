from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import tkinter as tk
from tkinter import ttk
import streamlit as st

client_id = "c4d29e11f8a44dbab2ede3a248adabff"
client_secret = "b7a56a97217240debb03d310dfe7a5d1"
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# === 1. Definisikan fungsi dulu ===
def get_track_info(track_ids):
    tracks = []
    for tid in track_ids:
        try:
            track = sp.track(tid)
            info = {
                'track_id': tid,
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'popularity': track['popularity']
            }
            tracks.append(info)
        except:
            print(f"Gagal ambil data untuk {tid}")
    return pd.DataFrame(tracks)

df = pd.read_csv("top_100_spotify.csv", encoding='utf-8', on_bad_lines='skip')

st.title("🎵 Rekomendasi 100 Lagu Paling Banyak Diputar")

# Input pencarian dari user
query = st.text_input("Cari Berdasarkan Judul Lagu atau Nama Artis:")

# Filter data berdasarkan input
if query:
    filtered_df = df[
        df['title'].str.contains(query, case=False, na=False) |
        df['artist'].str.contains(query, case=False, na=False)
    ]
    st.write(f"Hasil Pencarian Untuk: {query}")
    st.dataframe(filtered_df.reset_index(drop=True))
else:
    st.write("Menampilkan Semua Lagu:")
    st.dataframe(df)