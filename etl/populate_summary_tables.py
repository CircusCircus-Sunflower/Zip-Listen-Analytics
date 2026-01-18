"""
Populate ALL summary tables (idempotent).

- Uses UPSERT (ON CONFLICT DO UPDATE) so reruns refresh rows instead of duplicating.
- Does NOT TRUNCATE by default.

Run:
  python etl/populate_summary_tables.py

Optional (danger): reset tables first
  python etl/populate_summary_tables.py --reset
"""

import os
import sys
import argparse
from sqlalchemy import create_engine, text


# ----------------------------
# Helpers
# ----------------------------
REGION_CASE = """
CASE
  WHEN state IN ('CT','ME','MA','NH','RI','VT','NJ','NY','PA') THEN 'Northeast'
  WHEN state IN ('DE','FL','GA','MD','NC','SC','VA','DC','WV','AL','KY','MS','TN','AR','LA','TX') THEN 'Southeast'
  WHEN state IN ('IL','IN','MI','OH','WI','IA','KS','MN','MO','NE','ND','SD') THEN 'Midwest'
  WHEN state IN ('AZ','CA','CO','ID','MT','NV','NM','OR','UT','WA','WY','AK','HI') THEN 'West'
  ELSE 'Unknown'
END
"""

DEVICE_CASE = """
CASE
  WHEN "userAgent" ILIKE '%ipad%' OR "userAgent" ILIKE '%tablet%' THEN 'tablet'
  WHEN "userAgent" ILIKE '%iphone%' OR "userAgent" ILIKE '%android%' OR "userAgent" ILIKE '%mobile%' THEN 'mobile'
  WHEN "userAgent" ILIKE '%windows%' OR "userAgent" ILIKE '%macintosh%' OR "userAgent" ILIKE '%linux%' THEN 'desktop'
  ELSE 'unknown'
END
"""

def get_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # fallback (edit if needed)
        db_url = "postgresql://sunflower_user:password@localhost:5432/sunflower"
    return create_engine(db_url)

def table_columns(conn, table_name: str):
    q = text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema='public' AND table_name=:t
        ORDER BY ordinal_position
    """)
    return [r[0] for r in conn.execute(q, {"t": table_name}).fetchall()]

def reset_tables(conn):
    # Only summary tables, not raw event tables.
    tables = [
        "summary_artist_popularity_by_geo",
        "summary_city_growth_trends",
        "summary_genre_by_region",
        "summary_platform_usage",
        "summary_retention_cohort",
        "summary_subscribers_by_region",
        "summary_user_engagement_by_content",
    ]
    for t in tables:
        conn.execute(text(f"TRUNCATE TABLE public.{t} RESTART IDENTITY;"))
    conn.commit()


# ----------------------------
# 1) Platform usage (device_type + region)
# ----------------------------
def load_platform_usage(conn):
    sql = f"""
    INSERT INTO summary_platform_usage (device_type, region_name, active_users, play_count, last_updated)
    SELECT
      {DEVICE_CASE} AS device_type,
      COALESCE(region, {REGION_CASE}) AS region_name,
      COUNT(DISTINCT "userId")::int AS active_users,
      COUNT(*)::int AS play_count,
      NOW() AS last_updated
    FROM listen_events
    WHERE "userId" IS NOT NULL
    GROUP BY 1, 2
    ON CONFLICT (device_type, region_name)
    DO UPDATE SET
      active_users = EXCLUDED.active_users,
      play_count   = EXCLUDED.play_count,
      last_updated = NOW();
    """
    conn.execute(text(sql))
    conn.commit()


# ----------------------------
# 2) City growth trends (monthly)
# ----------------------------
def load_city_growth_trends(conn):
    sql = """
    WITH monthly AS (
      SELECT
        city,
        state,
        DATE_TRUNC('month', to_timestamp(ts/1000.0))::date AS date,
        COUNT(DISTINCT "userId")::int AS new_users,
        ROUND(SUM(duration)/3600.0)::int AS total_streaming_hours
      FROM listen_events
      WHERE city IS NOT NULL AND state IS NOT NULL AND "userId" IS NOT NULL
      GROUP BY city, state, DATE_TRUNC('month', to_timestamp(ts/1000.0))::date
    ),
    with_prev AS (
      SELECT
        m.*,
        LAG(new_users) OVER (PARTITION BY city, state ORDER BY date) AS prev_users
      FROM monthly m
    )
    INSERT INTO summary_city_growth_trends
      (city, state, date, new_users, percent_growth_wow, total_streaming_hours, last_updated)
    SELECT
      city,
      state,
      date,
      new_users,
      CASE
        WHEN prev_users IS NULL OR prev_users = 0 THEN NULL
        ELSE ROUND(((new_users - prev_users)::numeric / prev_users) * 100, 1)
      END AS percent_growth_wow,
      total_streaming_hours,
      NOW() AS last_updated
    FROM with_prev
    ON CONFLICT (city, state, date)
    DO UPDATE SET
      new_users = EXCLUDED.new_users,
      percent_growth_wow = EXCLUDED.percent_growth_wow,
      total_streaming_hours = EXCLUDED.total_streaming_hours,
      last_updated = NOW();
    """
    conn.execute(text(sql))
    conn.commit()


# ----------------------------
# 3) Retention cohort (monthly cohorts, period = months since cohort start)
# NOTE: Your table columns are (cohort_month, period, churned_users, upgrades, downgrades, last_updated)
# Here, "churned_users" is actually counting active users in that cohort for that period (matches what you were doing).
# ----------------------------
def load_retention_cohort(conn):
    sql = """
    WITH first_seen AS (
      SELECT
        "userId" AS user_id,
        DATE_TRUNC('month', MIN(to_timestamp(ts/1000.0)))::date AS cohort_month
      FROM listen_events
      WHERE "userId" IS NOT NULL
      GROUP BY "userId"
    ),
    activity AS (
      SELECT
        "userId" AS user_id,
        DATE_TRUNC('month', to_timestamp(ts/1000.0))::date AS activity_month
      FROM listen_events
      WHERE "userId" IS NOT NULL
      GROUP BY "userId", DATE_TRUNC('month', to_timestamp(ts/1000.0))::date
    ),
    joined AS (
      SELECT
        fs.cohort_month,
        (
          (EXTRACT(YEAR FROM a.activity_month) - EXTRACT(YEAR FROM fs.cohort_month)) * 12
          + (EXTRACT(MONTH FROM a.activity_month) - EXTRACT(MONTH FROM fs.cohort_month))
        )::int AS period,
        a.user_id
      FROM first_seen fs
      JOIN activity a
        ON a.user_id = fs.user_id
    )
    INSERT INTO summary_retention_cohort
      (cohort_month, period, churned_users, upgrades, downgrades, last_updated)
    SELECT
      cohort_month::text AS cohort_month,
      period,
      COUNT(DISTINCT user_id)::int AS churned_users,
      0::int AS upgrades,
      0::int AS downgrades,
      NOW() AS last_updated
    FROM joined
    WHERE period >= 0
    GROUP BY cohort_month, period
    ON CONFLICT (cohort_month, period)
    DO UPDATE SET
      churned_users = EXCLUDED.churned_users,
      upgrades = EXCLUDED.upgrades,
      downgrades = EXCLUDED.downgrades,
      last_updated = NOW();
    """
    conn.execute(text(sql))
    conn.commit()


# ----------------------------
# 4) Genre by region
# ----------------------------
def load_genre_by_region(conn):
    sql = f"""
    INSERT INTO summary_genre_by_region (region_name, genre, listen_count, last_updated)
    SELECT
      COALESCE(region, {REGION_CASE}) AS region_name,
      genre,
      COUNT(*)::int AS listen_count,
      NOW() AS last_updated
    FROM listen_events
    WHERE state IS NOT NULL AND genre IS NOT NULL
    GROUP BY 1, 2
    ON CONFLICT (region_name, genre)
    DO UPDATE SET
      listen_count = EXCLUDED.listen_count,
      last_updated = NOW();
    """
    conn.execute(text(sql))
    conn.commit()


# ----------------------------
# 5) Subscribers by region (uses status_change_events)
# ----------------------------
def load_subscribers_by_region(conn):
    sql = f"""
    INSERT INTO summary_subscribers_by_region (region_name, level, subscriber_count, last_updated)
    SELECT
      {REGION_CASE} AS region_name,
      level,
      COUNT(DISTINCT "userId")::int AS subscriber_count,
      NOW() AS last_updated
    FROM status_change_events
    WHERE state IS NOT NULL AND level IS NOT NULL AND "userId" IS NOT NULL
    GROUP BY 1, 2
    ON CONFLICT (region_name, level)
    DO UPDATE SET
      subscriber_count = EXCLUDED.subscriber_count,
      last_updated = NOW();
    """
    conn.execute(text(sql))
    conn.commit()


# ----------------------------
# 6) Artist popularity by geo (top artist per state)
# ----------------------------
def load_artist_popularity_by_geo(conn):
    sql = """
    WITH agg AS (
      SELECT
        state,
        artist,
        COUNT(*)::int AS play_count,
        COUNT(DISTINCT "userId")::int AS unique_listeners
      FROM listen_events
      WHERE state IS NOT NULL AND artist IS NOT NULL AND "userId" IS NOT NULL
      GROUP BY state, artist
    ),
    ranked AS (
      SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY state ORDER BY play_count DESC, unique_listeners DESC, artist ASC) AS rn
      FROM agg
    )
    INSERT INTO summary_artist_popularity_by_geo (state, artist, play_count, unique_listeners, last_updated)
    SELECT
      state, artist, play_count, unique_listeners, NOW()
    FROM ranked
    WHERE rn = 1
    ON CONFLICT (state, artist)
    DO UPDATE SET
      play_count = EXCLUDED.play_count,
      unique_listeners = EXCLUDED.unique_listeners,
      last_updated = NOW();
    """
    conn.execute(text(sql))
    conn.commit()


# ----------------------------
# 7) User engagement by content
# Because your exact columns weren’t shown, this function adapts to common column names.
# It will:
#   - compute engagement at the SONG level (artist + song)
#   - load into whatever columns exist that match the pattern
# ----------------------------
def load_user_engagement_by_content(conn):
    table = "summary_user_engagement_by_content"
    cols = table_columns(conn, table)

    # We’ll compute a “content_key” and then map into whatever your table calls it.
    # Common possibilities: content_name, content, content_key, item_name, song, track, etc.
    if "content_name" in cols:
        content_col = "content_name"
    elif "content" in cols:
        content_col = "content"
    elif "content_key" in cols:
        content_col = "content_key"
    else:
        # last resort: if your table doesn't have a place to store content, fail loudly
        raise RuntimeError(
            f"{table} columns are {cols}. Add a content column (e.g., content_name) so we can load it."
        )

    # Optional columns
    has_content_type = "content_type" in cols
    has_region = "region_name" in cols
    has_play_count = "play_count" in cols or "plays" in cols
    has_unique = "unique_listeners" in cols or "unique_users" in cols
    has_hours = "total_streaming_hours" in cols or "streaming_hours" in cols

    play_col = "play_count" if "play_count" in cols else ("plays" if "plays" in cols else None)
    unique_col = "unique_listeners" if "unique_listeners" in cols else ("unique_users" if "unique_users" in cols else None)
    hours_col = "total_streaming_hours" if "total_streaming_hours" in cols else ("streaming_hours" if "streaming_hours" in cols else None)

    select_parts = []
    insert_cols = []

    if has_content_type:
        insert_cols.append("content_type")
        select_parts.append("'song'::text AS content_type")

    insert_cols.append(content_col)
    # content_key: "Artist - Song"
    select_parts.append("""(COALESCE(artist,'Unknown') || ' - ' || COALESCE(song,'Unknown'))::text AS content_key""")

    if has_region:
        insert_cols.append("region_name")
        select_parts.append(f"COALESCE(region, {REGION_CASE}) AS region_name")

    if play_col:
        insert_cols.append(play_col)
        select_parts.append("COUNT(*)::int AS plays")

    if unique_col:
        insert_cols.append(unique_col)
        select_parts.append('COUNT(DISTINCT "userId")::int AS unique_listeners')

    if hours_col:
        insert_cols.append(hours_col)
        select_parts.append("ROUND(SUM(duration)/3600.0)::int AS streaming_hours")

    insert_cols.append("last_updated")
    select_parts.append("NOW() AS last_updated")

    group_by = []
    idx = 1
    if has_content_type:
        group_by.append(str(idx))  # content_type literal
        idx += 1
    group_by.append(str(idx))      # content_key
    idx += 1
    if has_region:
        group_by.append(str(idx))  # region_name
        idx += 1

    # Build ON CONFLICT target from PK if possible
    # If your PK is different, adjust this list.
    conflict_cols = []
    if has_content_type:
        conflict_cols.append("content_type")
    conflict_cols.append(content_col)
    if has_region:
        conflict_cols.append("region_name")

    update_sets = []
    if play_col:
        update_sets.append(f"{play_col} = EXCLUDED.{play_col}")
    if unique_col:
        update_sets.append(f"{unique_col} = EXCLUDED.{unique_col}")
    if hours_col:
        update_sets.append(f"{hours_col} = EXCLUDED.{hours_col}")
    update_sets.append("last_updated = NOW()")

    sql = f"""
    INSERT INTO {table} ({", ".join(insert_cols)})
    SELECT
      {", ".join(select_parts)}
    FROM listen_events
    WHERE "userId" IS NOT NULL
    GROUP BY {", ".join(group_by)}
    ON CONFLICT ({", ".join(conflict_cols)})
    DO UPDATE SET
      {", ".join(update_sets)};
    """
    # Replace our alias name to match chosen column name
    # content_key alias must match the insert column name
    sql = sql.replace("AS content_key", f"AS {content_col}")

    conn.execute(text(sql))
    conn.commit()


# ----------------------------
# Main
# ----------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="TRUNCATE summary tables before loading (DANGEROUS).")
    args = parser.parse_args()

    engine = get_engine()
    with engine.connect() as conn:
        if args.reset:
            reset_tables(conn)

        load_platform_usage(conn)
        load_city_growth_trends(conn)
        load_retention_cohort(conn)
        load_genre_by_region(conn)
        load_subscribers_by_region(conn)
        load_artist_popularity_by_geo(conn)
        load_user_engagement_by_content(conn)

    engine.dispose()
    print("✅ All summary tables populated.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ ETL failed: {e}", file=sys.stderr)
        sys.exit(1)
