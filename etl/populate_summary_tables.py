import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@host:port/dbname")

def load_artist_popularity():
    """Populate summary_artist_popularity_by_geo table."""
    listen_events = pd.read_sql("""
        SELECT state, artist, COUNT(*) AS play_count, COUNT(DISTINCT userId) AS unique_listeners
        FROM listen_events
        GROUP BY state, artist
    """, engine)

    top_artist_by_state = (
        listen_events.sort_values('play_count', ascending=False)
        .groupby('state')
        .head(1)
    )

    for _, row in top_artist_by_state.iterrows():
        engine.execute("""
            INSERT INTO summary_artist_popularity_by_geo (state, artist, play_count, unique_listeners, last_updated)
            VALUES (%s, %s, %s, %s, NOW())
            ON CONFLICT (state, artist) 
            DO UPDATE SET play_count=EXCLUDED.play_count, unique_listeners=EXCLUDED.unique_listeners, last_updated=NOW();
        """, (row['state'], row['artist'], int(row['play_count']), int(row['unique_listeners'])))

def load_genre_by_region():
    """Populate summary_genre_by_region table."""
    listen_events = pd.read_sql("""
        SELECT state, genre, COUNT(*) AS stream_count
        FROM listen_events
        GROUP BY state, genre
    """, engine)
    # Map state to region if needed, then insert per region/genre.
    for _, row in listen_events.iterrows():
        engine.execute("""
            INSERT INTO summary_genre_by_region (state, genre, stream_count, last_updated)
            VALUES (%s, %s, %s, NOW())
            ON CONFLICT (state, genre)
            DO UPDATE SET stream_count=EXCLUDED.stream_count, last_updated=NOW();
        """, (row['state'], row['genre'], int(row['stream_count'])))

def load_subscriber_by_region():
    """Populate summary_subscriber_by_region table."""
    # Replace with your actual user/subscriber table, e.g., status_change_events
    subscribers = pd.read_sql("""
        SELECT state, level, COUNT(DISTINCT userId) AS user_count
        FROM status_change_events
        GROUP BY state, level
    """, engine)
    for _, row in subscribers.iterrows():
        engine.execute("""
            INSERT INTO summary_subscriber_by_region (state, level, user_count, last_updated)
            VALUES (%s, %s, %s, NOW())
            ON CONFLICT (state, level)
            DO UPDATE SET user_count=EXCLUDED.user_count, last_updated=NOW();
        """, (row['state'], row['level'], int(row['user_count'])))

if __name__ == "__main__":
    print("Populating all summary tables...")
    load_artist_popularity()
    load_genre_by_region()
    load_subscriber_by_region()
    # add more summary loads/functions here as needed
    engine.dispose()
    print("All summary tables populated!")
