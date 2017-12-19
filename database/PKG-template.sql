/* Clear out previous rows before inserting */
DELETE FROM packages WHERE pkgid="PKGID";

INSERT INTO packages VALUES (
    /* pkgid */         'PKGID',
    /* pkg_date */      'PKGDATE',
    /* location */      'LOCATION',
    /* subjects */      'SUBJECTS',
    /* media_type */    'MEDIA_TYPE',               /* 'print', 'negative' */
    /* media_fmt */     'MEDIA_FMT',                /* 'roll', 'print', 'slide' */
    /* media_status */  'MEDIA_STATUS',             /* 'complete', 'partial' */
    /* film */          'FILM',
    /* sequence */      'SEQUENCE',
    /* frames */        0,
    /* pieces */        0,
    /* sheets */        0,
    /* set_date */      'SET_DATETIME',
    /* interval */      60,                         /* seconds */
    /* description */   ''
);

/* Clear out previous rows before inserting. */
DELETE FROM photographs WHERE pkgid="PKGID";

/* Insert individual photo descriptions. */
INSERT INTO photographs VALUES (
    /* pkgid */         'PKGID',
    /* photoid */       'PKGID-F00',
    /* poi */           0,
    /* description */   ''
);

