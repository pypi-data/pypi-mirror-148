import numpy as np
import seaborn as sns
import pandas as pd

from ..util import plot_each_col
from tickcounter import statistics, plot
from tickcounter.config import *

import itertools

class Survey(object):
    def __init__(self, data, *,num_col=None, cat_col=None, description=None):
        self.data = data
        self.num_col = num_col
        self.cat_col = cat_col
        self.descrip = description

    def auto_detect(self, cohen_es=COHEN_ES, eta=ETA, phi_es=PHI_ES, p_value=P_VALUE, min_sample=MIN_SAMPLE):
        findings_list = statistics._auto_detect(data=self.data, 
                                                num_col=self.num_col, 
                                                cat_col=self.cat_col,
                                                cohen_es=cohen_es,
                                                eta=eta,
                                                phi_es=phi_es,
                                                p_value=p_value,
                                                min_sample=min_sample)
        findings_list.set_descrip(self.descrip)
        return findings_list
    
    def anova(self, num_col, group_col):
        return statistics._anova(self.data, num_col, group_col)
    
    def compute_eta_squared(self, *args):
        return statistics._compute_eta_squared(self, *args)
    
    def compare_mean(self, num_col, group_col, *, cohen_es=COHEN_ES, eta=ETA, p_value=P_VALUE, min_sample=MIN_SAMPLE):
        # TODO: Do we want to expose this method? Because it return None when nothing happens
        return statistics._compare_mean(self.data, 
                                        num_col, 
                                        group_col, 
                                        cohen_es=cohen_es, 
                                        eta=eta, 
                                        p_value=p_value,
                                        min_sample=min_sample)

    def compare_group(self, col_1, col_2, p_value=P_VALUE, phi_es=PHI_ES, min_sample=MIN_SAMPLE):
        return statistics._compare_group(data=self.data,
                                         col_1=col_1,
                                         col_2=col_2, 
                                         p_value=p_value,
                                         phi_es=phi_es,
                                         min_sample=min_sample)

    def t_test(self, num_col, group_col, group_1=None, group_2=None, **kwargs):
        return statistics._t_test(data=self.data,
                                  num_col=num_col,
                                  group_col=group_col,
                                  group_1=group_1,
                                  group_2=group_2,
                                  **kwargs)
    
    def compute_cohen_es(self, sample_1, sample_2):
        return statistics._compute_cohen_es(sample_1, sample_2)
    
    def compute_phi_es(self, chi2, n):
        return statistics._compute_phi_es(chi2, n)
    
    def chi_squared(self, col_1, expected=None):
        return statistics._chi_squared(self.data, col_1, expected)
    
    def chi_squared_dependence(self, col_1, col_2, groups_1=None, groups_2=None, min_sample=MIN_SAMPLE):
        return statistics._chi_squared_dependence(self.data, col_1, col_2, groups_1, groups_2, min_sample)

    def hist_num(self, **kwargs):
        return self._plot(columns=self.num_col, kind='hist', **kwargs)
    
    def box_num(self, **kwargs):
        return self._plot(columns=self.num_col, kind='box', **kwargs)
    
    def count_cat(self, **kwargs):
        return self._plot(columns=self.cat_col, kind='count', **kwargs)
    
    def locate_outlier(self, columns, method='iqr', return_rule=False, zscore_threshold=3):
        if method == 'iqr':
            outlier, outlier_range =  statistics._locate_outlier_iqr(data=self.data, columns=columns)
        elif method == 'zscore':
            outlier, outlier_range = statistics._locate_outlier_zscore(data=self.data, columns=columns, zscore_threshold=zscore_threshold)
        else:
            raise ValueError("method argument can only be either 'iqr" or 'zscore')

        if return_rule:
            return outlier, outlier_range
        else:
            return outlier
    
    def scatter_num(self, **kwargs):
        return sns.pairplot(data=self.data, vars=self.num_col, kind='scatter', **kwargs)
    
    def compare_dist(self, feat_1, feat_2, **kwargs):
        return plot.compare_dist(self.data, feat_1, feat_2, descrip=self.descrip, **kwargs)
    
    def crosstab(self, index, col):
        # Should be a label paired with an info columns
        return pd.crosstab(self.data[index], self.data[col])
    
    def drop(self, index):
        self.data.drop(index, inplace=True)
    
    def _plot(self, columns, kind, **kwargs):
        return plot.plot_each_col(data=self.data, 
                                  col_list=columns, 
                                  plot_type=kind, 
                                  descrip=self.descrip, 
                                  **kwargs)

    def _handle_null(self, data, col):
        return data.dropna(subset=col)