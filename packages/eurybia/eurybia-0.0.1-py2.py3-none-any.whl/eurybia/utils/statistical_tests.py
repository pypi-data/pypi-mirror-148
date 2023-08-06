"""
Statistical test functions
"""
import numpy as np
import pandas as pd
from scipy import stats


def ksmirnov_test(obs_a: np.array, obs_b: np.array) -> dict:
    """
    Returns a dict containing testname, statistic, pvalue of the ks test

    Parameters
    ----------
    obs_a : np.array
        1D array containing the feature values in the first sample
    obs_b : np.array
        1D array containing the feature values ​​in the second sample

    Returns
    -------
    dict :
        3 keys : testname, statistic, pvalue
    """
    test_result = stats.ks_2samp(obs_a, obs_b)
    output = {"testname": "K-Smirnov", "statistic": test_result.statistic, "pvalue": test_result.pvalue}
    return output


def chisq_test(obs_a: np.array, obs_b: np.array) -> dict:
    """
    Returns a dict containing testname, statistic, pvalue of the chisquare test

    Parameters
    ----------
    obs_a : np.array
        1D array containing the feature values in the first sample
    obs_b : np.array
        1D array containing the feature values ​​in the second sample

    Returns
    -------
    dict :
        3 keys : testname, statistic, pvalue
    """
    uniq_a, freq_a = np.unique(obs_a, return_counts=True)
    freq_a_df = pd.DataFrame(freq_a, index=uniq_a, columns=["a"])

    uniq_b, freq_b = np.unique(obs_b, return_counts=True)
    freq_b_df = pd.DataFrame(freq_b, index=uniq_b, columns=["b"])

    freq = pd.concat([freq_a_df, freq_b_df], axis=1).transpose().to_numpy(na_value=0)

    g, p, _, _ = stats.chi2_contingency(freq)

    output = {"testname": "Chi-Square", "statistic": g, "pvalue": p}
    return output
