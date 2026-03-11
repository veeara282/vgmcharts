BEGIN;

-- Convenience view mapping recordings to artists, including recording details and artist details.
CREATE VIEW recordings_artists AS
SELECT DISTINCT
    r.recording_id,
    r.recording_title,
    r.duration_ms,
    r.isrc,
    r.franchise_id,
    r.category,
    a.artist_id,
    a.artist_name,
    a.spotify_artist_id,
    a.slug AS artist_slug
FROM recordings r
JOIN tracks t
    ON t.recording_id = r.recording_id
JOIN tracks_artists ta
    ON ta.track_id = t.track_id
JOIN artists a
    ON a.artist_id = ta.artist_id;

COMMIT;
