"""
Unit test statistical_tests.py
"""
import unittest

import numpy as np

from eurybia.utils.statistical_tests import chisq_test, ksmirnov_test


class TestStatistical_tests(unittest.TestCase):
    """
    Unit test statistical_tests.py
    """

    def test_ksmirnov_test(self):
        """
        Unit test ksmirnov_test function
        """
        X1 = np.array([0, 3, 9857, 3444, 99, 8, 9, 9, 0, 4535, 34])
        X2 = np.array([0.45, 3, 9857, 3444, 4535, 34])

        res = ksmirnov_test(X1, X2)

        assert res["testname"] == "K-Smirnov"
        assert round(res["statistic"], 2) == 0.23
        assert round(res["pvalue"], 2) == 0.95

    def test_chisq_test(self):
        """
        Unit test chisq_test function
        """
        X1 = np.array([0, 0, 3, 4, 2, 2, 2, 2, 2, 1])
        X2 = np.array([3, 4, 3, 2, 1])

        res = chisq_test(X1, X2)

        assert res["testname"] == "Chi-Square"
        assert round(res["statistic"], 2) == 3.75
        assert round(res["pvalue"], 2) == 0.44
