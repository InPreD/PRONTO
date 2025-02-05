import math
import pronto.pronto
import pandas
import pytest

from contextlib import nullcontext as does_not_raise

@pytest.mark.parametrize(
    "input, exception, want",
    [
        (
            pandas.DataFrame({
                'AF_tumor_DNA': [0.3, 0.5, 0.7],
                'Change_summary': ['c.10A>G:exon1:S10G:Ser10Gly', 'c.10A>G:exon1:NA:NA', float('nan')],
                'DNA_change': ['c.4C>G', 'c.5C>G', 'c.6C>G'],
                'Depth_tumor_DNA': [1000, 1500, 2000],
                'Genomic_location': ['1:100', '1:200', '1:300'],
                'RefSeq_mRNA': ['NM_000001', 'NM_000002', 'NM_000003'],
                'cDNA_change': ['c.4C>G', 'c.5C>G', 'c.6C>G']
            }),
            does_not_raise(),
            pandas.DataFrame({
                'AF_tumor_DNA': ['30.0%', '50.0%', '70.0%'],
                'Change_summary': ['c.10A>G,p.(S10G),p.(Ser10Gly)', 'c.10A>G', float('nan')],
                'DNA_change': ['c.4C>G', 'c.5C>G', 'c.6C>G'],
                'Depth_tumor_DNA': [1000, 1500, 2000],
                'Genomic_location': ['1:100', '1:200', '1:300'],
                'RefSeq_mRNA': ['NM_000001', 'NM_000002', 'NM_000003'],
                'cDNA_change': ['c.4C>G', 'c.5C>G', 'c.6C>G'],
                'Genomic coordinates in hg19 build': ['chr1:g.100c.4C>G', 'chr1:g.200c.5C>G', 'chr1:g.300c.6C>G'],
                'HGVS syntax': ['NM_000001:c.4C>G', 'NM_000002:c.5C>G', 'NM_000003:c.6C>G'],
                'Read depth(variant reads/total reads)': ['300/1000', '750/1500', '1400/2000']
            })
        ),
    ]
)
def test_create_mtb_columns(input, exception, want):
    with exception:
        pandas.testing.assert_frame_equal(pronto.pronto.create_mtb_columns(input), want)

@pytest.mark.parametrize(
    "input, exception, want",
    [
        (
            pandas.DataFrame({
                'str1': ['a'],
                'str2': ['a']
            }),
            does_not_raise(),
            [['str1\t', 'str2\n'], ['a\t', 'a\n']]
        ),
        (
            pandas.DataFrame({
                'int': [1]
            }),
            does_not_raise(),
            [['int\n'], ['1\n']]
        ),
        (
            pandas.DataFrame({
                'float': [1.5, 2.6]
            }),
            does_not_raise(),
            [['float\n'], ['1.5\n'], ['2.6\n']]
        ),
    ]
)
def test_dataframe_to_list(input, exception, want):
    with exception:
        assert pronto.pronto.dataframe_to_list(input) == want

@pytest.mark.parametrize(
    "input, exception, want",
    [
        (0.5, does_not_raise(), '50.0%'),
        (0.30678, does_not_raise(), '30.7%')
    ]
)
def test_format_af_tumor_dna(input, exception, want):
    with exception:
        assert pronto.pronto.format_af_tumor_dna(input) == want

@pytest.mark.parametrize(
    "input, exception, want",
    [
        ('c.2797A>G:exon14:S933G:Ser933Gly', does_not_raise(), 'c.2797A>G,p.(S933G),p.(Ser933Gly)'),
        ('c.2797A>G:exon14:NA:NA', does_not_raise(), 'c.2797A>G'),
        (float('nan'), does_not_raise(), float('nan')),
    ]
)
def test_format_change_summary(input, exception, want):
    with exception:
        if isinstance(input, float):
            assert math.isnan(input)
        else:
            assert pronto.pronto.format_change_summary(input) == want

@pytest.mark.parametrize(
    "input1, input2, exception, want",
    [
        ('1:100', 'c.4C>G', does_not_raise(), 'chr1:g.100c.4C>G'),
    ]
)
def test_format_genomic_coordinates(input1, input2, exception, want):
    with exception:
        assert pronto.pronto.format_genomic_coordinates(input1, input2) == want

@pytest.mark.parametrize(
    "input1, input2, exception, want",
    [
        ('NM_000001', 'c.4G>C', does_not_raise(), 'NM_000001:c.4G>C'),
    ]
)
def test_format_hgvs_syntax(input1, input2, exception, want):
    with exception:
        assert pronto.pronto.format_hgvs_syntax(input1, input2) == want

@pytest.mark.parametrize(
    "input, exception, want",
    [
        ('C135W', does_not_raise(), ',p.(C135W)'),
        ('Cys135Trp', does_not_raise(), ',p.(Cys135Trp)'),
        ('NA', does_not_raise(), ''),
    ]
)
def test_format_prot_change(input, exception, want):
    with exception:
        assert pronto.pronto.format_prot_change(input) == want

@pytest.mark.parametrize(
    "input1,, input2, exception, want",
    [
        (1000, 0.3, does_not_raise(), '300/1000'),
        (1001, 0.3, does_not_raise(), '300/1001'),
    ]
)
def test_format_read_depth(input1, input2, exception, want):
    with exception:
        assert pronto.pronto.format_read_depth(input1, input2) == want

@pytest.mark.parametrize(
    "input, exception, want",
    [
        (-1, does_not_raise(), "-1 mut/Mb; Not available\n"),
        (2.5, does_not_raise(), "2.5 mut/Mb; lav\n"),
        (7, does_not_raise(), "7 mut/Mb; intermediær\n"),
        (23, does_not_raise(), "23 mut/Mb; høy\n")
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
                'pronto/tests/data/hus/',
                '250101_NDX012345_RUO_0001_01234ABCDE',
                'IPH0001-D01-R01-A01',
            ),
            does_not_raise(),
            'pronto/tests/data/hus/250101_NDX012345_RUO_0001_01234ABCDE/250101_NDX012345_RUO_0001_01234ABCDE_ppr/IPH0001-D01-R01-A01'
        ),
        (
            (
                'pronto/tests/data/none',
                'existent',
                'test.txt'
            ),
            pytest.raises(ValueError),
            None
        ),
        (
            (
                'pronto/tests/data/*',
                '250101_NDX012345_RUO_0001_01234ABCDE',
                'IPH0001-D01-R01-A01',
                'test.txt'
            ),
            pytest.raises(ValueError),
            None
        ),
    ]
)
def test_glob_tsoppi_file(inputs, exception, want):
    with exception:
        assert pronto.pronto.glob_tsoppi_file(*inputs) == want

@pytest.mark.parametrize(
    "input, exception, want",
    [
        ('LikSOM,SOM,LikGL,incon,include', does_not_raise(), {'exclude': '', 'include': 'LikSOM|SOM|LikGL|incon|include'}),
        ('!x:noncoding_variant && !synonymous_variant', does_not_raise(), {'exclude': 'x:noncoding_variant|synonymous_variant', 'include': ''}),
        ('!x:noncoding_variant', does_not_raise(), {'exclude': 'x:noncoding_variant', 'include': ''}),
        ('BioMar,VUSpot,AddRes,GLrel', does_not_raise(), {'exclude': '', 'include': 'BioMar|VUSpot|AddRes|GLrel'})
    ]
)
def test_parse_keys(input, exception, want):
    with exception:
        assert pronto.pronto.parse_keys(input) == want