import pytest
from pydantic import ValidationError

from knowitall.domain import BusinessScope, ScopeSource


def test_explicit_scope_requires_at_least_one_business_line() -> None:
    with pytest.raises(ValidationError):
        BusinessScope(source=ScopeSource.USER_EXPLICIT, business_line_ids=[])


def test_explicit_scope_is_valid_with_a_business_line() -> None:
    scope = BusinessScope(
        source=ScopeSource.USER_EXPLICIT,
        business_line_ids=["commerce-order"],
        confidence=1.0,
    )
    assert scope.business_line_ids == ["commerce-order"]
