import pytest
import pronto.pronto

from contextlib import nullcontext as does_not_raise

@pytest.mark.parametrize(
    "input, exception, want",
    [
        (-1, does_not_raise(), "-1 mut/Mb; Not available\n"),
        (2.5, does_not_raise(), "2.5 mut/Mb; lav\n"),
        (7, does_not_raise(), "7 mut/Mb; intermediær\n"),
        (23, does_not_raise(), "23 mut/Mb; høy\n"),
    ]
)
def test_get_tmb_string(input, exception, want):
    with exception:
        assert pronto.pronto.get_tmb_string(input) == want