from mxm.foundry.checks.registry import misc_checks, policy_check_codes
from tests.checks.expected import EXPECTED_POLICY_CHECK_CODES


def test_policy_check_codes_contains_license_policy_checks() -> None:
    assert policy_check_codes() == EXPECTED_POLICY_CHECK_CODES


def test_misc_checks_exclude_policy_checks() -> None:
    codes = {check.code for check in misc_checks()}

    assert codes.isdisjoint(EXPECTED_POLICY_CHECK_CODES)
