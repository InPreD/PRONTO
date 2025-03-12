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

@pytest.mark.parametrize(
    "inputs, exception, want",
    [
        (
            (
                True,
                'pronto/tests/data/ous',
                '250101_NDX012345_RUO_0001_01234ABCDE',
                'IPH0001-D01-R01-A01',
                'test.txt'
            ),
            does_not_raise(),
            'pronto/tests/data/ous/250101_NDX012345_RUO_0001_01234ABCDE_TSO_500_LocalApp_postprocessing_results/IPH0001-D01-R01-A01/test.txt'
        ),
        (
            (
                True,
                'pronto/tests/data/hus/',
                '250101_NDX012345_RUO_0001_01234ABCDE',
                'IPH0001-D01-R01-A01',
                'test*.txt'
            ),
            does_not_raise(),
            'pronto/tests/data/hus/250101_NDX012345_RUO_0001_01234ABCDE/250101_NDX012345_RUO_0001_01234ABCDE_ppr/IPH0001-D01-R01-A01/test.txt'
        ),
        (
            (
                True,
                'pronto/tests/data/hus/',
                '250101_NDX012345_RUO_0001_01234ABCDE',
                'IPH0001-D01-R01-A01',
                'tes*.txt'
            ),
            does_not_raise(),
            'pronto/tests/data/hus/250101_NDX012345_RUO_0001_01234ABCDE/250101_NDX012345_RUO_0001_01234ABCDE_ppr/IPH0001-D01-R01-A01/test.txt'
        ),
        (
            (
                True,
                'pronto/tests/data/hus/',
                '250101_NDX012345_RUO_0001_01234ABCDE',
                'IPH0001-D01-R01-A01',
            ),
            does_not_raise(),
            'pronto/tests/data/hus/250101_NDX012345_RUO_0001_01234ABCDE/250101_NDX012345_RUO_0001_01234ABCDE_ppr/IPH0001-D01-R01-A01'
        ),
        (
            (
                True,
                'pronto/tests/data/none',
                'existent',
                'test.txt'
            ),
            pytest.raises(ValueError),
            None
        ),
        (
            (
                True,
                'pronto/tests/data/*',
                '250101_NDX012345_RUO_0001_01234ABCDE',
                'IPH0001-D01-R01-A01',
                'test.txt'
            ),
            pytest.raises(ValueError),
            None
        ),
        (
            (
                False,
                'pronto/tests/data/*',
                '250101_NDX012345_RUO_0001_01234ABCDE',
                'IPH0001-D01-R01-A01',
                'test.txt'
            ),
            does_not_raise(),
            None
        ),
    ]
)
def test_glob_tsoppi_file(inputs, exception, want):
    with exception:
        assert pronto.pronto.glob_tsoppi_file(*inputs) == want
