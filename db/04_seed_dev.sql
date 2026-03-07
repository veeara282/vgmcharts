-- Development seed data for vgmcharts
-- Mix of real and synthetic development data.

BEGIN;

INSERT INTO franchises (franchise_id, franchise_name)
VALUES
    (0, 'Unknown Franchise'),
    (151, 'Pokémon')
ON CONFLICT (franchise_id) DO NOTHING;

INSERT INTO artists (artist_name, spotify_artist_id, slug)
VALUES
    ('Pokémon', '6goK4KMSdP4A8lw8jk4ADk', 'pokemon-official'),
    ('GlitchxCity', '0X1wtVNo8CVrMEKh8y8knH', 'glitchxcity'),
    ('Jonathan Young', '2IeMt1qx6ZVt1HFjdfE5tl', 'jonathan-young'),
    ('Jason Paige', '4C2BnfCRMI8bTf3LlBUljz', 'jason-paige'),
    ('Ben Dixon and the Sad Truth', '6ep1x3L37GYJ8IHVORMgGj', 'ben-dixon-and-the-sad-truth'),
    ('Ed Goldfarb', '20v1pWVDGh4qNUlJeoCGef', 'ed-goldfarb'),
    ('Cam Steady', '0v2ThByhPk4mutkJNv6mue', 'cam-steady'),
    ('Ty Wild', '2uE23RLfCmZurbJzYgjKMm', 'ty-wild'),
    ('Cindery', '7uRrPnto4j1qfkBcTv3iKL', 'cindery'),
    ('PokéLoFi Collective', NULL, 'pokelofi-collective'),
    ('No Copyright Music', NULL, 'no-copyright-music')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO releases (
    release_title,
    short_description,
    franchise_id,
    release_type,
    release_date,
    total_tracks,
    spotify_album_id,
    upc,
    label_name,
    copyright_c,
    copyright_p
)
VALUES
    (
        'Pokémon: 2.B.A. Master (Music from the TV Series)',
        'Official soundtrack album for the early Pokémon animated series.',
        151,
        'album',
        DATE '1999-06-29',
        13,
        '0xdrSLNEZnhSkaYJHnXJyY',
        '8721215934677',
        'Laced Records',
        '1999 Pokémon',
        '1999 Pokémon under license to Laced Music Ltd t/a Laced Records'
    ),
    (
        'Levincia',
        'Single by GlitchxCity based on the Pokémon Scarlet and Violet city theme.',
        151,
        'single',
        DATE '2024-12-06',
        1,
        '15KpbH3zOW41tc3PkY46cj',
        '199097449127',
        'GlitchxCity',
        '2024 GlitchxCity',
        '2024 GlitchxCity'
    ),
    (
        'PokéJon',
        'Jonathan Young release containing Pokémon-inspired covers.',
        151,
        'compilation',
        DATE '2017-12-12',
        10,
        '2zd9KnWtSZaveHirW4lJFG',
        '192378254052',
        'Jonathan Young',
        '2017 Youngster Multimedia',
        '2017 Youngster Multimedia'
    ),
    (
        'TEAM YELL',
        'Team Yell tribute single by Cam Steady.',
        151,
        'single',
        DATE '2024-05-24',
        1,
        '73dErkosgaI4b4TCJDYr3S',
        '198657549352',
        'Cam Steady, Inc.',
        '2024 Cam Steady, Inc.',
        '2024 Cam Steady, Inc.'
    ),
    (
        'Pokemon Sleep Covers EP',
        'Synthetic dev EP for frontend testing; note the title uses Pokemon without the accent.',
        151,
        'ep',
        DATE '2025-02-14',
        3,
        'dev_album_001',
        NULL,
        'Team Rocket Records',
        '2025 Team Rocket Records',
        '2025 Team Rocket Records'
    ),
    (
        'Pokémon Horizons Fan Mixes',
        'Synthetic compilation used to exercise compilation pages and mixed artist credits.',
        151,
        'compilation',
        DATE '2025-08-01',
        4,
        'dev_album_002',
        NULL,
        'Team Skull Records',
        '2025 Team Skull Records',
        '2025 Team Skull Records'
    ),
    (
        'Mystery Zone Lofi Remix',
        'Mysterious single with no copyright notice.',
        151,
        'single',
        DATE '2025-12-31',
        1,
        'dev_album_003',
        NULL,
        'No Copyright Music',
        NULL,
        NULL
    )
ON CONFLICT DO NOTHING;

INSERT INTO release_artwork (release_id, source, url, width, height)
SELECT r.release_id, 'dev_seed', CONCAT('https://example.com/artwork/', r.release_id, '.jpg'), 640, 640
FROM releases r
ON CONFLICT DO NOTHING;

INSERT INTO release_artists (release_id, artist_id, artist_role, artist_order)
VALUES
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokémon: 2.B.A. Master (Music from the TV Series)'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Pokémon'),
        'primary',
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Levincia'),
        (SELECT artist_id FROM artists WHERE artist_name = 'GlitchxCity'),
        'primary',
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'PokéJon'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Jonathan Young'),
        'primary',
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokemon Sleep Covers EP'),
        (SELECT artist_id FROM artists WHERE artist_name = 'PokéLoFi Collective'),
        'primary',
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'TEAM YELL'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Cam Steady'),
        'primary',
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokémon Horizons Fan Mixes'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Pokémon'),
        'primary',
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Mystery Zone Lofi Remix'),
        (SELECT artist_id FROM artists WHERE artist_name = 'No Copyright Music'),
        'primary',
        1
    )
ON CONFLICT DO NOTHING;

INSERT INTO recordings (
    recording_title,
    duration_ms,
    isrc,
    franchise_id,
    category
)
VALUES
    (
        'Pokémon Theme',
        198000,
        'USKO10406205',
        151,
        'official'
    ),
    (
        'Levincia',
        193000,
        'QZZ7T2426404',
        151,
        'fan_cover'
    ),
    (
        'Pokémon Theme',
        222000,
        'QZAPG1706347',
        151,
        'fan_cover'
    ),
    (
        'Pokemon Center Theme (Lo-Fi Lullaby Remix)',
        176000,
        'XADEV2500001',
        151,
        'fan_cover'
    ),
    (
        'Littleroot Town (Sleep Mix)',
        201000,
        'XADEV2500002',
        151,
        'fan_cover'
    ),
    (
        'Battle! Gym Leader (Midnight Version)',
        187000,
        'XADEV2500003',
        151,
        'fan_cover'
    ),
    (
        'TEAM YELL',
        189000,
        'QZMEQ2467320',
        151,
        'fan_song'
    ),
    (
        'Pokemon Theme (Arcade Mix)',
        214000,
        'XADEV2500005',
        151,
        'fan_cover'
    ),
    (
        'Pokémon Theme (Version XY)',
        207000,
        'XADEV2500006',
        151,
        'official'
    ),
    (
        'Levincia (Night Drive Edit)',
        205000,
        'XADEV2500007',
        151,
        'fan_cover'
    ),
    (
        'Pokemon Trainer Anthem',
        211000,
        'XADEV2500008',
        151,
        'fan_song'
    ),
    (
        'Mystery Zone Lofi Remix',
        238000,
        'XADEV2500009',
        151,
        'fan_cover'
    )
ON CONFLICT DO NOTHING;

INSERT INTO tracks (
    release_id,
    recording_id,
    spotify_track_id,
    disc_number,
    track_number
)
VALUES
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokémon: 2.B.A. Master (Music from the TV Series)'),
        (SELECT recording_id FROM recordings WHERE isrc = 'USKO10406205'),
        '3mNH9BXFcNElEFbgKqmq1J',
        1,
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Levincia'),
        (SELECT recording_id FROM recordings WHERE isrc = 'QZZ7T2426404'),
        '2b5JwljPJyBZZDRaDmFImu',
        1,
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'PokéJon'),
        (SELECT recording_id FROM recordings WHERE isrc = 'QZAPG1706347'),
        '6qlz1QARHfChlLCmWYrOKu',
        1,
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokemon Sleep Covers EP'),
        (SELECT recording_id FROM recordings WHERE isrc = 'XADEV2500001'),
        'dev_track_001',
        1,
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokemon Sleep Covers EP'),
        (SELECT recording_id FROM recordings WHERE isrc = 'XADEV2500002'),
        'dev_track_002',
        1,
        2
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokemon Sleep Covers EP'),
        (SELECT recording_id FROM recordings WHERE isrc = 'XADEV2500003'),
        'dev_track_003',
        1,
        3
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'TEAM YELL'),
        (SELECT recording_id FROM recordings WHERE isrc = 'QZMEQ2467320'),
        '57lrVtQWflD12qWGPXge9x',
        1,
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokémon Horizons Fan Mixes'),
        (SELECT recording_id FROM recordings WHERE isrc = 'XADEV2500005'),
        'dev_track_005',
        1,
        1
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokémon Horizons Fan Mixes'),
        (SELECT recording_id FROM recordings WHERE isrc = 'XADEV2500006'),
        'dev_track_006',
        1,
        2
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokémon Horizons Fan Mixes'),
        (SELECT recording_id FROM recordings WHERE isrc = 'XADEV2500007'),
        'dev_track_007',
        1,
        3
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Pokémon Horizons Fan Mixes'),
        (SELECT recording_id FROM recordings WHERE isrc = 'XADEV2500008'),
        'dev_track_008',
        1,
        4
    ),
    (
        (SELECT release_id FROM releases WHERE release_title = 'Mystery Zone Lofi Remix'),
        (SELECT recording_id FROM recordings WHERE isrc = 'XADEV2500009'),
        'dev_track_009',
        1,
        1
    )
ON CONFLICT DO NOTHING;

INSERT INTO tracks_artists (track_id, artist_id, artist_role, artist_order)
VALUES
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'USKO10406205'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'Pokémon: 2.B.A. Master (Music from the TV Series)')),
        (SELECT artist_id FROM artists WHERE artist_name = 'Pokémon'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZZ7T2426404'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'Levincia')),
        (SELECT artist_id FROM artists WHERE artist_name = 'GlitchxCity'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZAPG1706347'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'PokéJon')),
        (SELECT artist_id FROM artists WHERE artist_name = 'Jonathan Young'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZAPG1706347'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'PokéJon')),
        (SELECT artist_id FROM artists WHERE artist_name = 'Jason Paige'),
        'featured',
        2
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500001'),
        (SELECT artist_id FROM artists WHERE artist_name = 'GlitchxCity'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500002'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Cindery'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500003'),
        (SELECT artist_id FROM artists WHERE artist_name = 'PokéLoFi Collective'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZMEQ2467320'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Cam Steady'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZMEQ2467320'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Ty Wild'),
        'featured',
        2
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500005'),
        (SELECT artist_id FROM artists WHERE artist_name = 'PokéLoFi Collective'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500006'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Pokémon'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500006'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Ben Dixon and the Sad Truth'),
        'featured',
        2
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500006'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Ed Goldfarb'),
        'featured',
        3
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500007'),
        (SELECT artist_id FROM artists WHERE artist_name = 'GlitchxCity'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500008'),
        (SELECT artist_id FROM artists WHERE artist_name = 'Cam Steady'),
        'primary',
        1
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500009'),
        (SELECT artist_id FROM artists WHERE artist_name = 'No Copyright Music'),
        'primary',
        1
    )
ON CONFLICT DO NOTHING;

INSERT INTO tracks_popularity (track_id, dt, spotify_popularity)
VALUES
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'USKO10406205'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'Pokémon: 2.B.A. Master (Music from the TV Series)')),
        TIMESTAMPTZ '2026-03-01 00:00:00+00',
        68
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'USKO10406205'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'Pokémon: 2.B.A. Master (Music from the TV Series)')),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        69
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZZ7T2426404'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'Levincia')),
        TIMESTAMPTZ '2026-03-01 00:00:00+00',
        41
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZZ7T2426404'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'Levincia')),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        44
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZAPG1706347'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'PokéJon')),
        TIMESTAMPTZ '2026-03-01 00:00:00+00',
        53
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZAPG1706347'
           AND t.release_id = (SELECT release_id FROM releases WHERE release_title = 'PokéJon')),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        55
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500001'),
        TIMESTAMPTZ '2026-03-01 00:00:00+00',
        36
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500001'),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        39
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500002'),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        28
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500003'),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        24
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZMEQ2467320'),
        TIMESTAMPTZ '2026-03-01 00:00:00+00',
        31
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'QZMEQ2467320'),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        34
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500005'),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        22
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500006'),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        47
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500007'),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        26
    ),
    (
        (SELECT t.track_id
         FROM tracks t
         JOIN recordings r ON r.recording_id = t.recording_id
         WHERE r.isrc = 'XADEV2500008'),
        TIMESTAMPTZ '2026-03-05 00:00:00+00',
        19
    )
ON CONFLICT DO NOTHING;

COMMIT;
