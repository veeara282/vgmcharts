-- Enforce cross-table data constraints before adding development seed data
BEGIN;

-- =========================================================
-- Release must have at least one artist
-- =========================================================

CREATE OR REPLACE FUNCTION check_release_has_artist()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_release_id INTEGER;
    v_title TEXT;
    v_upc TEXT;
BEGIN
    v_release_id := COALESCE(NEW.release_id, OLD.release_id);

    IF NOT EXISTS (
        SELECT 1
        FROM release_artists ra
        WHERE ra.release_id = v_release_id
    ) THEN
        SELECT r.release_title, r.upc
        INTO v_title, v_upc
        FROM releases r
        WHERE r.release_id = v_release_id;

        RAISE EXCEPTION
            'release % ("%"; UPC=%) must have at least one artist',
            v_release_id,
            COALESCE(v_title, '<missing release>'),
            COALESCE(v_upc, 'NULL');
    END IF;

    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER release_must_have_artist_after_release
AFTER INSERT OR UPDATE ON releases
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_release_has_artist();

CREATE CONSTRAINT TRIGGER release_must_have_artist_after_release_artist_change
AFTER INSERT OR UPDATE OR DELETE ON release_artists
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_release_has_artist();


-- =========================================================
-- Release must have at least one track
-- =========================================================

CREATE OR REPLACE FUNCTION check_release_has_track()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_release_id INTEGER;
    v_title TEXT;
    v_upc TEXT;
BEGIN
    v_release_id := COALESCE(NEW.release_id, OLD.release_id);

    IF NOT EXISTS (
        SELECT 1
        FROM tracks t
        WHERE t.release_id = v_release_id
    ) THEN
        SELECT r.release_title, r.upc
        INTO v_title, v_upc
        FROM releases r
        WHERE r.release_id = v_release_id;

        RAISE EXCEPTION
            'release % ("%"; UPC=%) must have at least one track',
            v_release_id,
            COALESCE(v_title, '<missing release>'),
            COALESCE(v_upc, 'NULL');
    END IF;

    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER release_must_have_track_after_release
AFTER INSERT OR UPDATE ON releases
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_release_has_track();

CREATE CONSTRAINT TRIGGER release_must_have_track_after_track_change
AFTER INSERT OR UPDATE OR DELETE ON tracks
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_release_has_track();


-- =========================================================
-- Recording must be connected to at least one track
-- =========================================================

CREATE OR REPLACE FUNCTION check_recording_has_track()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_recording_id INTEGER;
    v_title TEXT;
    v_isrc TEXT;
BEGIN
    v_recording_id := COALESCE(NEW.recording_id, OLD.recording_id);

    IF NOT EXISTS (
        SELECT 1
        FROM tracks t
        WHERE t.recording_id = v_recording_id
    ) THEN
        SELECT rec.recording_title, rec.isrc
        INTO v_title, v_isrc
        FROM recordings rec
        WHERE rec.recording_id = v_recording_id;

        RAISE EXCEPTION
            'recording % ("%"; ISRC=%) must be connected to at least one track',
            v_recording_id,
            COALESCE(v_title, '<missing recording>'),
            COALESCE(v_isrc, 'NULL');
    END IF;

    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER recording_must_have_track_after_recording
AFTER INSERT OR UPDATE ON recordings
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_recording_has_track();

CREATE CONSTRAINT TRIGGER recording_must_have_track_after_track_change
AFTER INSERT OR UPDATE OR DELETE ON tracks
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_recording_has_track();


-- =========================================================
-- Track must have at least one artist
-- =========================================================

CREATE OR REPLACE FUNCTION check_track_has_artist()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_track_id INTEGER;
    v_release_id INTEGER;
    v_track_number INTEGER;
    v_disc_number INTEGER;
    v_spotify_track_id TEXT;
    v_release_title TEXT;
    v_recording_title TEXT;
BEGIN
    v_track_id := COALESCE(NEW.track_id, OLD.track_id);

    IF NOT EXISTS (
        SELECT 1
        FROM tracks_artists ta
        WHERE ta.track_id = v_track_id
    ) THEN
        SELECT
            t.release_id,
            t.track_number,
            t.disc_number,
            t.spotify_track_id,
            r.release_title,
            rec.recording_title
        INTO
            v_release_id,
            v_track_number,
            v_disc_number,
            v_spotify_track_id,
            v_release_title,
            v_recording_title
        FROM tracks t
        JOIN releases r
          ON r.release_id = t.release_id
        JOIN recordings rec
          ON rec.recording_id = t.recording_id
        WHERE t.track_id = v_track_id;

        RAISE EXCEPTION
            'track % (release=% "%", disc=% track=%, recording="%", spotify_track_id=%) must have at least one artist',
            v_track_id,
            COALESCE(v_release_id, -1),
            COALESCE(v_release_title, '<missing release>'),
            COALESCE(v_disc_number, -1),
            COALESCE(v_track_number, -1),
            COALESCE(v_recording_title, '<missing recording>'),
            COALESCE(v_spotify_track_id, 'NULL');
    END IF;

    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER track_must_have_artist_after_track
AFTER INSERT OR UPDATE ON tracks
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_track_has_artist();

CREATE CONSTRAINT TRIGGER track_must_have_artist_after_track_artist_change
AFTER INSERT OR UPDATE OR DELETE ON tracks_artists
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_track_has_artist();

COMMIT;
