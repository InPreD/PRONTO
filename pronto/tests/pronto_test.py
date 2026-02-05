import pandas
import pytest
import pronto.pronto

from contextlib import nullcontext as does_not_raise

@pytest.mark.parametrize(
    "input, exception, want",
    [
        (-1, does_not_raise(), "-1 mut/Mb; Not available\n"),
        (2.5, does_not_raise(), "2.5 mut/Mb; Lav\n"),
        (7, does_not_raise(), "7 mut/Mb; Intermediær\n"),
        (23, does_not_raise(), "23 mut/Mb; Høy\n"),
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

@pytest.mark.parametrize(
    "inputs, exception, want",
    [
        (
            (
                pandas.DataFrame({
                    "one": [1, 2],
                    "two": [3, 4],
                    "three": [5, 6],
                    "four": [7, 8],
                }),
                ["one", "two", "three", "four"],
            ),
            does_not_raise(),
            pandas.DataFrame({
                "one": [1, 2],
                "two": [3, 4],
                "three": [5, 6],
                "four": [7, 8],
            }),
        ),
        (
            (
                pandas.DataFrame({
                    "one": [1, 2],
                    "two": [3, 4],
                    "four": [7, 8],
                }),
                ["one", "two", "three", "four"],
            ),
            does_not_raise(),
            pandas.DataFrame({
                "one": [1, 2],
                "two": [3, 4],
                "three": [' ', ' '],
                "four": [7, 8],
            }),
        ),
        (
            (
                pandas.DataFrame({
                    "one": [1, 2],
                    "two": [3, 4],
                    "three": [5, 6],
                    "four": [7, 8],
                }),
                ["two", "three", "four"],
            ),
            does_not_raise(),
            pandas.DataFrame({
                "two": [3, 4],
                "three": [5, 6],
                "four": [7, 8],
                "one": [1, 2],
            }),
        ),
        (
            (
                pandas.DataFrame({
                    "one": [1, 2],
                    "two": [3, 4],
                    "four": [7, 8],
                    "five": [9, 10],
                }),
                ["one", "two", "three", "four"],
            ),
            does_not_raise(),
            pandas.DataFrame({
                "one": [1, 2],
                "two": [3, 4],
                "three": [' ', ' '],
                "four": [7, 8],
                "five": [9, 10],
            }),
        ),
    ]
)
def test_normalize_column_index(inputs, exception, want):
    with exception:
        get = pronto.pronto.normalize_column_index(*inputs)
        assert want.equals(get)

@pytest.mark.parametrize(
    "inputs, exception, want",
    [
        (
            (
                pandas.DataFrame({
                    "one": [1, 2],
                    "two": [3.333, 4.444],
                }),
                "two",
            ),
            does_not_raise(),
            pandas.DataFrame({
                "one": [1, 2],
                "two": ["3.33", "4.44"],
            }),
        ),
        (
            (
                pandas.DataFrame({
                    "one": [1, 2],
                    "two": ['3.666', '4.777'],
                }),
                "two",
            ),
            does_not_raise(),
            pandas.DataFrame({
                "one": [1, 2],
                "two": ["3.67", "4.78"],
            }),
        ),
        (
            (
                pandas.DataFrame({
                    "one": [1, 2],
                }),
                "two",
            ),
            does_not_raise(),
            pandas.DataFrame({
                "one": [1, 2],
            }),
        ),
    ]
)
def test_set_column_to_2_decimals(inputs, exception, want):
    with exception:
        get = pronto.pronto.set_column_to_2_decimals(*inputs)
        assert want.equals(get)