import pytest
import requests

from pandas import DataFrame

from dataretrieval.nwis import query_waterservices, get_record

def test_query_waterservices_validation():
    """Tests the validation parameters of the query_waterservices method"""
    with pytest.raises(TypeError) as type_error:
        query_waterservices(service='dv', format='rdb')
    assert 'Query must specify a major filter: sites, stateCd, bBox' == str(type_error.value)

    with pytest.raises(TypeError) as type_error:
        query_waterservices(service=None, sites='sites')
    assert 'Service not recognized' == str(type_error.value)

def test_get_record_validation():
    """Tests the validation parameters of the get_record method"""
    with pytest.raises(TypeError) as type_error:
        get_record(sites=['01491000'], service='not_a_service')
    assert 'Unrecognized service: not_a_service' == str(type_error.value)

    with pytest.raises(TypeError) as type_error:
        get_record(sites=['01491000'], service='stat')
    assert 'stat service not yet implemented' == str(type_error.value)

def test_get_dv(requests_mock):
    """Tests get_dv method correctly generates the request url and returns the result in a DataFrame"""
    with open('data/waterservices_dv.json') as text:
        requests_mock.get('https://waterservices.usgs.gov/nwis/dv?format=json&sites=01491000%2C01645000'
                          '&startDT=2020-02-14&endDT=2020-02-15',
                          text=text.read())
    dv = get_record(sites=["01491000","01645000"], start='2020-02-14', end='2020-02-15', service='dv')
    assert type(dv) is DataFrame

def test_get_iv(requests_mock):
    """Tests get_dv method correctly generates the request url and returns the result in a DataFrame"""
    with open('data/waterservices_iv.json') as text:
        requests_mock.get('https://waterservices.usgs.gov/nwis/iv?sites=01491000%2C01645000&format=json'
                          '&startDT=2020-02-14&endDT=2020-02-15',
                          text=text.read())
    iv = get_record(sites=["01491000","01645000"], start='2020-02-14', end='2020-02-15', service='iv')
    assert type(iv) is DataFrame

def test_get_info(requests_mock):
    """
    Tests get_info method correctly generates the request url and returns the result in a DataFrame.
    Note that only sites and format are passed as query params
    """
    with open('data/waterservices_site.txt') as text:
        requests_mock.get('https://waterservices.usgs.gov/nwis/site?sites=01491000%2C01645000&format=rdb',
                          text=text.read())
    info = get_record(sites=["01491000","01645000"], start='2020-02-14', end='2020-02-15', service='site')
    assert type(info) is DataFrame


def test_get_qwdata():
    """Tests get_qwdata method correctly generates the request url and returns the result in a DataFrame"""
    #with open('data/waterdata_qwdata.txt') as text:
    #    requests_mock.get('https://nwis.waterdata.usgs.gov/nwis/qwdata?agency_cd=USGS&format=rdb'
    #                      '&pm_cd_compare=Greater+than&inventory_output=0&rdb_inventory_output=file&TZoutput=0'
    #                      '&radio_parm_cds=all_parm_cds&rdb_qw_attributes=expanded&date_format=YYYY-MM-DD'
    #                      '&rdb_compression=value&submmitted_form=brief_list&site_no=01491000%2C01645000'
    #                      '&qw_sample_wide=separated_wide',
    #                      text=text.read())
    info = get_record(sites=["01491000","01645000"], service='qwdata')
    assert type(info) is DataFrame


def test_get_gwlevels(requests_mock):
    """Tests get_gwlevels method correctly generates the request url and returns the result in a DataFrame."""
    with open('data/waterservices_gwlevels.txt') as text:
        requests_mock.get('https://waterservices.usgs.gov/nwis/gwlevels?sites=434400121275801&format=rdb',
                          text=text.read())

    gwlevels = get_record(sites=["434400121275801"], service='gwlevels')
    assert type(gwlevels) is DataFrame
