import pandas as pd
import numpy as np
from scipy import stats

class DataAnalysis:
    def __init__(self, connection):
        self.connection = connection

    def fetch_data(self, query):
        df = pd.read_sql(query, self.connection)
        return df

    def analyze_data(self, df):
        analysis_results = {}
        analysis_results['mean'] = df.mean()
        analysis_results['std'] = df.std()

        # 回歸直線
        regression = linregress(df['x'], df['y'])
        analysis_results['slope'] = regression.slope
        analysis_results['intercept'] = regression.intercept
        analysis_results['r_value'] = regression.rvalue
        analysis_results['p_value'] = regression.pvalue
        analysis_results['std_err'] = regression.stderr

        df['regression_line'] = regression.intercept + regression.slope * df['x']
        
        return df, analysis_results

