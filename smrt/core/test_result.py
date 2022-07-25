# coding: utf-8

import copy
import numpy as np
import xarray as xr
from smrt.core import result


# Tests written in response to -ve intensity bug in result.py
res_example = result.ActiveResult([[[[4.01445680e-03, 3.77746658e-03, 0.00000000e+00]],
                                    [[3.83889082e-03, 3.85904771e-03, 0.00000000e+00]],
                                    [[2.76453599e-20, -2.73266027e-20, 0.00000000e+00]]]],
                                  coords=[('theta', [35]), ('polarization', ['V', 'H', 'U']),
                                          ('theta_inc', [35]), ('polarization_inc', ['V', 'H', 'U'])],
                                  channel_map={'VV': dict(polarization='V', polarization_inc='V'),
                                               'VH': dict(polarization='H', polarization_inc='V')})

res_example2 = result.ActiveResult([[[[4e-03, 3e-03, 0]],
                                     [[3e-03, 3.85904771e-03, 0]],
                                     [[0, 0, 0.00000000e+00]]]],
                                   coords=[('theta', [45]), ('polarization', ['V', 'H', 'U']),
                                           ('theta_inc', [45]), ('polarization_inc', ['V', 'H', 'U'])],
                                   channel_map={'VV': dict(polarization='V', polarization_inc='V'),
                                                'VH': dict(polarization='H', polarization_inc='V')})


def test_methods():
    assert hasattr(res_example, "sigma")
    assert not hasattr(res_example, "Tb")


def test_positive_sigmaVV():
    assert res_example.sigmaVV() > 0


def test_positive_sigmaVH():
    assert res_example.sigmaVH() > 0


def test_positive_sigmaHV():
    assert res_example.sigmaHV() > 0


def test_positive_sigmaHH():
    assert res_example.sigmaHH() > 0


def test_sigma_dB():
    np.testing.assert_allclose(res_example.sigmaVV_dB(), -13.8379882755357)
    np.testing.assert_allclose(res_example.sigmaHH_dB(), -14.0094546848676)
    np.testing.assert_allclose(res_example.sigmaHV_dB(), -14.102249856026)
    np.testing.assert_allclose(res_example.sigmaVH_dB(), -14.0321985560285)


def test_sigma_dB_as_dataframe():
    df = res_example.sigma_dB_as_dataframe(channel_axis='column')

    assert 'VV' in df.columns
    assert 'VH' in df.columns

    np.testing.assert_allclose(df['VV'], -13.8379882755357)
    np.testing.assert_allclose(df['VH'], -14.0321985560285)


def test_to_dataframe_wtih_channel_axis_on_column():
    df = res_example.to_dataframe(channel_axis='column')

    assert 'VV' in df.columns
    assert 'VH' in df.columns

    np.testing.assert_allclose(df['VV'], -13.8379882755357)
    np.testing.assert_allclose(df['VH'], -14.0321985560285)


def test_to_dataframe_wtihout_channel_axis():
    df = res_example.to_dataframe(channel_axis=None)
    np.testing.assert_allclose(df.loc[(35, 'V', 'V'), :], -13.8379882755357)
    np.testing.assert_allclose(df.loc[(35, 'H', 'V'), :], -14.0321985560285)


def test_return_as_series():
    series = res_example.to_series()
    print(series)

    assert 'VV' in series.index
    assert 'VH' in series.index

    np.testing.assert_allclose(series.loc['VV'], -13.8379882755357)
    np.testing.assert_allclose(series.loc['VH'], -14.0321985560285)


def test_concat_results():

    allresult = result.concat_results((res_example, res_example2), coord=('dim0', [0, 1]))
    print(allresult)
    assert 'dim0' in allresult.data.dims
    assert len(allresult.data['dim0']) == 2


def test_concat_results_other_data():

    res = copy.deepcopy(res_example)
    res2 = copy.deepcopy(res_example2)

    res.other_data['other_value'] = xr.DataArray([0.1, 0.2], coords=[('layer', [0, 1])])

    res2.other_data['other_value'] = xr.DataArray([0.2, 0.3], coords=[('layer', [0, 1])])

    allresult = result.concat_results((res, res2), coord=('dim0', [0, 1]))

    assert allresult.other_data['other_value'].dims == ('dim0', 'layer')
