from mxm.foundry.checks.registry import misc_checks, policy_check_codes


def test_policy_check_codes_contains_license_policy_checks() -> None:
    assert policy_check_codes() == {"FS002", "LIC001"}


def test_misc_checks_exclude_policy_checks() -> None:
    codes = [check.code for check in misc_checks()]

    assert "FS002" not in codes
    assert "LIC001" not in codes
