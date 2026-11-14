"""Synthetic decision fixtures. No network, credentials or production effects.

Run: python3 decision_variant_fixtures.py
The predicates are application-policy examples, not Claude SDK interfaces.
"""
import json


def authorized_effect(trusted, proposed, now):
    return (
        trusted.get('verified') is True
        and trusted.get('approved') is True
        and trusted.get('expires_at', 0) > now
        and all(trusted.get(k) == proposed.get(k)
                for k in ('account', 'proposal_version', 'amount'))
    )


def validate_extraction(candidate, source):
    errors = []
    if not isinstance(candidate.get('amount'), (int, float)):
        errors.append('amount_shape')
    if candidate.get('currency') not in ('USD', 'EUR', 'GBP'):
        errors.append('currency_shape')
    if candidate.get('amount') != source.get('amount'):
        errors.append('amount_source_mismatch')
    return errors


def validate_ci_fixture(raw, expected_commit):
    """Declared fictional envelope, not a version-independent CLI schema."""
    envelope = json.loads(raw)
    if envelope.get('is_error') is not False:
        raise ValueError('process_or_runtime_error')
    findings = json.loads(envelope['result'])
    if findings.get('commit') != expected_commit:
        raise ValueError('stale_commit')
    if not isinstance(findings.get('findings'), list):
        raise ValueError('findings_shape')
    for item in findings['findings']:
        if not item.get('path') or not item.get('evidence'):
            raise ValueError('missing_source_evidence')
    return findings


def run():
    trusted = dict(verified=True, approved=True, expires_at=120,
                   account='A', proposal_version=2, amount=40)
    proposed = dict(account='A', proposal_version=2, amount=40)
    assert authorized_effect(trusted, proposed, 100)
    assert not authorized_effect(trusted, dict(proposed, account='B'), 100)
    assert not authorized_effect(trusted, dict(proposed, amount=80), 100)
    assert not authorized_effect(trusted, proposed, 121)
    print('FV-04: current bound approval accepted; target, amount and expiry flips rejected')
    assert validate_extraction(dict(amount=90, currency='USD'), dict(amount=90)) == []
    assert validate_extraction(dict(amount=900, currency='USD'), dict(amount=90)) == ['amount_source_mismatch']
    print('FV-21: schema-valid wrong amount rejected by source check')
    valid = json.dumps(dict(is_error=False, result=json.dumps(dict(commit='reviewed', findings=[]))))
    assert validate_ci_fixture(valid, 'reviewed')['findings'] == []
    for raw in ('not json', json.dumps(dict(is_error=True, result='')), valid):
        try:
            validate_ci_fixture(raw, 'changed' if raw == valid else 'reviewed')
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError('bad CI fixture silently accepted')
    print('FV-18: malformed envelope, runtime error and stale commit fail visibly')


if __name__ == '__main__':
    run()
