BEGIN;

-- Convenience view mapping recordings to artists, including recording details and
-- artist details.
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

-- Convenience view mapping recordings to their appearances on releases, including
-- recording details and release details.
-- Note that the copyright_c and copyright_p fields from releases are intentionally
-- excluded from this view, as copyright strings pertain to each release as a whole
-- rather than individual recordings.
CREATE VIEW recording_appearances AS
SELECT
    r.recording_id,
    r.recording_title,
    r.duration_ms,
    r.isrc,
    r.franchise_id,
    r.category,
    t.track_id,
    t.spotify_track_id,
    t.disc_number,
    t.track_number,
    rel.release_id,
    rel.release_title,
    rel.release_type,
    rel.release_date,
    rel.spotify_album_id,
    rel.upc,
    rel.ean,
    rel.jp_catalog_no,
    rel.label_name
FROM recordings r
JOIN tracks t
    ON t.recording_id = r.recording_id
JOIN releases rel
    ON rel.release_id = t.release_id;

-- Convenience view for getting the album artwork for a given track.
-- In addition to join keys, some fields (title, ISRC) are included for easier debugging.
CREATE VIEW track_release_artwork AS
SELECT
    r.recording_id,
    r.recording_title,
    r.isrc,
    t.track_id,
    rel.release_id,
    rel.release_title,
    ra.source AS artwork_source,
    ra.url AS artwork_url,
    ra.width AS artwork_width,
    ra.height AS artwork_height
FROM recordings r
JOIN tracks t
    ON t.recording_id = r.recording_id
JOIN releases rel
    ON rel.release_id = t.release_id
JOIN release_artwork ra
    ON ra.release_id = rel.release_id;

-- View that selects a single "canonical" release for each recording, based on release
-- type and release date. This is used to determine which album artwork to show for each
-- recording in the UI.
-- The logic for determining the canonical release is as follows:
-- 1. Singles are preferred over EPs, which are preferred over albums, which are
--    preferred over compilations, which are preferred over unknown release types.
-- 2. If there are multiple releases of the same type, the earliest release date is
--    preferred (with undated releases ranked last).
-- 3. If there are still multiple releases tied after applying the above rules,
--    release_id and track_id are used as tiebreakers to ensure a deterministic result.
-- Only one row should be returned per recording.
CREATE VIEW recording_canonical_release AS
SELECT *
FROM (
    SELECT
        r.recording_id,
        r.recording_title,
        r.isrc,
        t.track_id,
        rel.release_id,
        rel.release_title,
        rel.release_type,
        rel.release_date,
        ROW_NUMBER() OVER (
            PARTITION BY r.recording_id
            ORDER BY
                CASE rel.release_type
                    WHEN 'single' THEN 1
                    WHEN 'ep' THEN 2
                    WHEN 'album' THEN 3
                    WHEN 'compilation' THEN 4
                    ELSE 999
                END,
                rel.release_date ASC NULLS LAST,
                rel.release_id ASC,
                t.track_id ASC
        ) AS rn
    FROM recordings r
    JOIN tracks t
        ON t.recording_id = r.recording_id
    JOIN releases rel
        ON rel.release_id = t.release_id
) ranked
WHERE rn = 1;

-- Convenience view for getting the canonical album artwork for a given recording using
-- the method implemented in the recording_canonical_release view above.
-- In addition to join keys, some fields (title, ISRC) are included for easier debugging.
CREATE VIEW recording_canonical_artwork AS
SELECT
    cr.recording_id,
    cr.recording_title,
    cr.isrc,
    cr.track_id,
    cr.release_id,
    cr.release_title,
    cr.release_type,
    cr.release_date,
    ra.source AS artwork_source,
    ra.url AS artwork_url,
    ra.width AS artwork_width,
    ra.height AS artwork_height
FROM recording_canonical_release cr
JOIN release_artwork ra
    ON ra.release_id = cr.release_id;

COMMIT;
