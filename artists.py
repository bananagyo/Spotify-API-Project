import pandas as pd

artists = """The Weeknd
Taylor Swift
Post Malone
Billie Eilish
Rihanna
Ariana Grande
Drake
Kendrick Lamar
Dua Lipa
Coldplay
Justin Bieber
David Guetta
SZA
Bruno Mars
Eminem
Calvin Harris
Kanye West
Travis Scott
Ed Sheeran
Bad Bunny
Shakira
Sabrina Carpenter
Marshmello
Beyoncé
Harry Styles
Imagine Dragons
Maroon 5
Future
Miley Cyrus
Metro Boomin
Sia
OneRepublic
Benson Boone
Hozier
J Balvin
21 Savage
Doja Cat
Katy Perry
Lady Gaga
Lana Del Rey
Olivia Rodrigo
Khalid
Rauw Alejandro
Queen
Daddy Yankee
Elton John
Tiësto
Adele
Tommy Richman
The Chainsmokers
Arctic Monkeys
Pitbull
Chris Brown
Sam Smith
Peso Pluma
Playboi Carti
KAROL G
Nicki Minaj
Artemas
One Direction
Morgan Wallen
Tate McRae
Camila Cabello
Cris Mj
Halsey
Feid
Myke Towers
Bebe Rexha
Maluma
Shawn Mendes
Michael Jackson
The Neighbourhood
Black Eyed Peas
J. Cole
Gunna
Linkin Park
Charlie Puth
Swae Lee
Ozuna
Selena Gomez
XXXTENTACION
Ty Dolla $ign
Arijit Singh
Justin Timberlake
Teddy Swims
Ellie Goulding
USHER
Avicii
Madonna
Ne-Yo
AC/DC
Ava Max
Britney Spears
James Arthur
A$AP Rocky
FloyyMenor
Red Hot Chili Peppers
Don Omar
The Beatles
Manuel Turizo"""

# artists_list = artists.split("\n")

# df = pd.DataFrame(artists_list)

# df.to_csv("artists.csv", index=False)

with open("artists.csv") as f:
    for artist in f:
        print(artist.strip())
