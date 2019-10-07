/* Clear out previous rows before inserting */
DELETE FROM packages WHERE pkgid="{{ package["pkgid"] }}";

INSERT INTO packages VALUES (
    /* pkgid */         '{{ package["pkgid"] }}',
    /* sequence */      '{{ package["sequence"] }}',
    /* pkg_date */      'PKGDATE',
    /* location */      'LOCATION',
    /* subjects */      'SUBJECTS',
    /* media_type */    'MEDIA_TYPE',               /* 'print', 'negative' */
    /* media_fmt */     'MEDIA_FMT',                /* 'roll', 'print', 'slide' */
    /* media_status */  'MEDIA_STATUS',             /* 'complete', 'partial' */
    /* film */          'FILM',
    /* nonce */         'NONCE',
    /* frames */        0,
    /* pieces */        0,
    /* sheets */        0,
    /* set_date */      'SET_DATETIME',
    /* interval */      60,                         /* seconds */
    /* description */   ''
);

/* Clear out previous rows before inserting. */
DELETE FROM photographs WHERE pkgid="{{ package["pkgid"] }}";

/* Insert individual photo descriptions. */
{% for photoid in photographs.keys() %}
INSERT INTO photographs VALUES (
    /* pkgid */         '{{ package["pkgid"] }}',
    /* photoid */       '{{ photoid }}',
    /* crop */          '{{ photographs[photoid]["crop"] }}',
    /* poi */           0,
    /* description */   '{{ photographs[photoid]["description"]|safe }}'
);
{% endfor %}

