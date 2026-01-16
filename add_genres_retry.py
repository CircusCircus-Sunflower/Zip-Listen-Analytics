"""
Add genres to listen_events - WITH RETRY LOGIC
Handles connection drops from XO server.
"""

import time
import random
import requests
from requests.exceptions import RequestException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# XO Database
DATABASE_URL = "postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower"

# MusicBrainz prefers a descriptive User-Agent with contact info.
# Replace the email with your real email.
HEADERS = {"User-Agent": "SunflowerAnalytics/1.0 (your_email@example.com)"}

# Re-use HTTP connections to reduce random connection resets
session = requests.Session()

genre_cache = {}

# Re-use HTTP connections for stability/performance
session = requests.Session()


def get_engine():
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def retry_on_disconnect(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(
                    f"\n  Connection dropped, reconnecting (attempt {attempt + 2})..."
                )
                time.sleep(2)
            else:
                raise e


def get_artist_genre(artist_name, max_retries=5):
    if artist_name in genre_cache:
        return genre_cache[artist_name]

    search_url = "https://musicbrainz.org/ws/2/artist/"
    params = {"query": artist_name, "fmt": "json", "limit": 1}

    for attempt in range(1, max_retries + 1):
        try:
            response = session.get(
                search_url, params=params, headers=HEADERS, timeout=15
            )

            # Handle temporary errors / throttling
            if response.status_code in (429, 502, 503, 504):
                retry_after = response.headers.get("Retry-After")
                sleep_s = float(retry_after) if retry_after else min(2**attempt, 30)
                sleep_s += random.uniform(0, 0.5)
                print(f"(HTTP {response.status_code}, retrying in {sleep_s:.1f}s)")
                time.sleep(sleep_s)
                continue

            if not response.ok:
                genre_cache[artist_name] = None
                return None

            data = response.json()
            artists = data.get("artists") or []
            if not artists:
                genre_cache[artist_name] = None
                return None

            artist = artists[0]
            tags = artist.get("tags", []) or []

            if tags:
                genre_tags = [t for t in tags if t.get("count", 0) > 0]
                if genre_tags:
                    genre_tags.sort(key=lambda x: x.get("count", 0), reverse=True)
                    genre = genre_tags[0]["name"].title()
                    genre_cache[artist_name] = genre
                    return genre

            genre_cache[artist_name] = None
            return None

        except RequestException as e:
            # Connection reset / timeout / transient network hiccup
            if attempt == max_retries:
                print(f"  API Error (final): {e}")
                genre_cache[artist_name] = None
                return None

            sleep_s = min(2**attempt, 30) + random.uniform(0, 0.5)
            print(
                f"  API hiccup (attempt {attempt}/{max_retries}): {e} — retrying in {sleep_s:.1f}s"
            )
            time.sleep(sleep_s)

    genre_cache[artist_name] = None
    return None


def update_artist_genre(engine, artist_name, genre):
    def do_update():
        with engine.connect() as conn:
            conn.execute(
                text("UPDATE listen_events SET genre = :genre WHERE artist = :artist"),
                {"genre": genre, "artist": artist_name},
            )
            conn.commit()

    retry_on_disconnect(do_update)


def main():
    print("=" * 60)
    print("  ADDING GENRES (with retry logic)")
    print("=" * 60)

    engine = get_engine()

    def add_column():
        with engine.connect() as conn:
            conn.execute(
                text(
                    "ALTER TABLE listen_events ADD COLUMN IF NOT EXISTS genre VARCHAR(100)"
                )
            )
            conn.commit()

    retry_on_disconnect(add_column)
    print("✓ Genre column ready")

    def get_artists():
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                SELECT DISTINCT artist 
                FROM listen_events 
                WHERE artist IS NOT NULL
                AND (genre IS NULL OR genre = '')
                ORDER BY artist
            """)
            )
            return [row[0] for row in result]

    artists = retry_on_disconnect(get_artists)
    print(f"\nFound {len(artists):,} artists without genres")
    print("This will take a while... (Ctrl+C to stop)\n")

    genres_found = 0

    for i, artist in enumerate(artists, 1):
        print(f"[{i}/{len(artists)}] {artist}...", end=" ", flush=True)

        genre = get_artist_genre(artist)

        if genre:
            try:
                if i % 500 == 0:
                    engine = get_engine()
                    print("\n  (Refreshed connection)")

                update_artist_genre(engine, artist, genre)
                print(f"✓ {genre}")
                genres_found += 1
            except Exception as e:
                print(f"✗ DB Error: {e}")
                engine = get_engine()
        else:
            print("✗ Not found")

        time.sleep(1.1)

    print("\n" + "=" * 60)
    print(f"  DONE! Added genres to {genres_found} artists")
    print("=" * 60)


if __name__ == "__main__":
    main()
