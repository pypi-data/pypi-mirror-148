import pytest

from firepit.pgstorage import _rewrite_select


@pytest.mark.parametrize(
    'stmt, expected', [
        ('SELECT urls.value,     urls.id    FROM ((urls JOIN whatever))',
         'SELECT urls.* FROM ((urls JOIN whatever))'
        ),
        ('SELECT "observed-data".first_observed,     urls.value,     urls.id    FROM ((urls JOIN whatever))',
         'SELECT "observed-data".first_observed, urls.* FROM ((urls JOIN whatever))'
        ),
        ("SELECT file.name,     file.hashes.'SHA-1',     file.size     FROM whatever",
         'SELECT file.* FROM whatever'
        ),
        ('SELECT "network-traffic".id,     "network-traffic".src_port,     "network-traffic".src_ref.value     FROM whatever',
         'SELECT "network-traffic".* FROM whatever'
        ),
        ("SELECT DISTINCT process.pid,     process.name,     process.created,     process.creator_user_ref,     process.binary_ref,     process.id    FROM ((nt      JOIN __reflist ON ((nt.id = __reflist.target_ref)))      JOIN process ON ((__reflist.source_ref = process.id)))   WHERE (__reflist.ref_name = 'opened_connection_refs'::text)",
         "SELECT DISTINCT process.* FROM ((nt      JOIN __reflist ON ((nt.id = __reflist.target_ref)))      JOIN process ON ((__reflist.source_ref = process.id)))   WHERE (__reflist.ref_name = 'opened_connection_refs'::text)"
         ),
    ]
)
def test_rewrite_select(stmt, expected):
    assert _rewrite_select(stmt) == expected
