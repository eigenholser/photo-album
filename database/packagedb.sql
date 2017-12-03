CREATE TABLE packages (
    pkgid           varchar(50),
    pkg_date        varchar(50),
    location        varchar(1024),
    subjects        varchar(1024),
    media_type      varchar(50),        /* 'print', 'negative' */
    media_fmt       varchar(50),        /* 'roll', 'print', 'slide' */
    media_status    varchar(50),        /* 'complete', 'partial' */
    film            varchar(50),
    sequence        varchar(10),
    frames          int,
    pieces          int,
    sheets          int,
    set_datetime    varchar(50),        /* 1999-01-01 12:00:00 */
    interval        int,                /* seconds */
    description     text
);

CREATE UNIQUE INDEX packages_pkgid ON packages(pkgid);

CREATE TABLE photographs (
    pkgid           varchar(50),
    photoid         varchar(50),
    description     text,
    FOREIGN KEY(pkgid) REFERENCES packages(pkgid)
);

CREATE UNIQUE INDEX photographs_photoid ON photographs(photoid);
