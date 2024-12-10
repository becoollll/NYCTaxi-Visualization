# data_manager.py
import pandas as pd
import numpy as np
from pathlib import Path
import os
import scipy.stats as stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class DataManager:
    def __init__(self):
        self.ROOT_DIR = Path(__file__).parent
        self.DATA_PATH = os.path.join(self.ROOT_DIR, 'datasets', 'yellow_tripdata_2024-07.parquet')
        
        # processed df
        self.data = {
            'original': None,
            'cleaned': None,
            'transformed': None,
            'final': None,
            'pca_results': None
        }
        
        # analysis results
        self.analysis_results = {
            'cleaning_summary': None,
            'normality_tests': {},
            'transformation_results': {},
            'pca_summary': None,
            'outlier_summary': None,
            'time_summary': None  # New field for time-related statistics
        }
        
        self._initialize_processing()
    
    def _initialize_processing(self):
        self._load_data()
        self._clean_data()
        self._transform_data()
        self._remove_outliers()
        self._perform_pca()
    
    def _load_data(self):
        try:
            self.data['original'] = pd.read_parquet(self.DATA_PATH)
        except FileNotFoundError:
            print(f"Error: Could not find data file at {self.DATA_PATH}")
            self.data['original'] = pd.DataFrame()
    
    def _clean_data(self):
        df = self.data['original'].copy()
        initial_count = len(df)
        
        # convert datetime columns
        df.loc[:, 'tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], errors='coerce')
        df.loc[:, 'tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], errors='coerce')
        
        # remove missing values after datetime conversion
        df = df.dropna()
        after_datetime_count = len(df)
        
        # calculate time difference in seconds
        df.loc[:, 'time_difference'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()
        
        # filter valid time differences (>= 60 seconds)
        df = df.loc[df['time_difference'] >= 60]
        after_time_diff_count = len(df)
        
        # filter date range (only July 2024)
        df = df[
            (df['tpep_pickup_datetime'] >= '2024-07-01') & 
            (df['tpep_pickup_datetime'] < '2024-08-01')
        ]
        after_date_range_count = len(df)
        
        # apply other rules
        df = df[
            (df['VendorID'].isin([1, 2])) &
            (df['passenger_count'] > 0) &
            (df['trip_distance'] >= 0.1) &
            (df['PULocationID'].notna()) &
            (df['DOLocationID'].notna()) &
            (df['RatecodeID'].isin([1, 2, 3, 4, 5, 6])) &
            (df['store_and_fwd_flag'].isin(['Y', 'N'])) &
            (df['payment_type'].isin([1, 2, 3, 4, 5, 6])) &
            (df['fare_amount'] >= 0) &
            (df['extra'] >= 0) &
            (df['mta_tax'] == 0.5) &
            (df['improvement_surcharge'] >= 0) &
            (df['tip_amount'] >= 0) &
            (df['tolls_amount'] >= 0) &
            (df['total_amount'] >= 0) &
            (df['congestion_surcharge'] >= 0) &
            (df['Airport_fee'] >= 0)
        ]
        
        # drop time_difference
        df = df.drop(columns=['time_difference'])
        
        self.data['cleaned'] = df
        
        # store cleaning summary
        self.analysis_results['cleaning_summary'] = {
            'original_records': initial_count,
            'after_datetime_conversion': after_datetime_count,
            'after_time_difference': after_time_diff_count,
            'after_date_range': after_date_range_count,
            'cleaned_records': len(df),
            'removed_records': initial_count - len(df)
        }
        
        # store time-related summary
        self.analysis_results['time_summary'] = {
            'date_range': {
                'start': df['tpep_pickup_datetime'].min(),
                'end': df['tpep_pickup_datetime'].max()
            },
            'avg_trip_duration': df['tpep_dropoff_datetime'].sub(df['tpep_pickup_datetime']).mean(),
            'total_trips_by_date': df.groupby(df['tpep_pickup_datetime'].dt.date).size().to_dict()
        }

    def _transform_data(self):
        # data transformation for numerical features
        df = self.data['cleaned'].copy()
        features_to_transform = [
            'trip_distance', 'fare_amount', 'total_amount',
            'tip_amount', 'tolls_amount'
        ]
        
        for feature in features_to_transform:
            # sample data for testing (convert to Series first)
            sample_size = min(5000, len(df))
            sample_data = pd.Series(df[feature].sample(sample_size))
            
            # store original normality test
            orig_stat, orig_p = stats.shapiro(sample_data)
            
            # transformations
            transforms = {
                'log': np.log1p(df[feature]),
                'sqrt': np.sqrt(df[feature]),
                'boxcox': stats.boxcox(df[feature] + 1)[0]
            }
            
            # convert transformed data to Series and test normality
            transform_results = {'original': orig_p}
            for name, transformed_data in transforms.items():
                # convert to Series for sampling
                transformed_series = pd.Series(transformed_data)
                sample_transformed = transformed_series.sample(sample_size)
                stat, p_value = stats.shapiro(sample_transformed)
                transform_results[name] = p_value
            
            # store transformation results
            self.analysis_results['transformation_results'][feature] = transform_results
            
            # apply log transformation to the dataframe
            df[f'{feature}_log'] = transforms['log']
        
        self.data['transformed'] = df
    
    def _remove_outliers(self):
        df = self.data['transformed'].copy()
        features_to_clean = [
            'trip_distance_log', 'fare_amount_log', 'total_amount_log',
            'tip_amount_log', 'tolls_amount_log'
        ]
        
        outlier_counts = {}
        for col in features_to_clean:
            upper_bound = df[col].quantile(0.99)
            outliers = df[df[col] > upper_bound]
            outlier_counts[col] = len(outliers)
            df = df[df[col] <= upper_bound]
        
        self.data['final'] = df
        self.analysis_results['outlier_summary'] = outlier_counts
    
    def _perform_pca(self):
        df = self.data['final']
        features = [
            'trip_distance_log', 'fare_amount_log', 'total_amount_log',
            'tip_amount_log', 'tolls_amount_log'
        ]
        
        # standbardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[features])
        
        pca = PCA()
        X_pca = pca.fit_transform(X_scaled)
        
        # store results
        self.analysis_results['pca_summary'] = {
            'explained_variance_ratio': pca.explained_variance_ratio_,
            'cumulative_variance_ratio': np.cumsum(pca.explained_variance_ratio_),
            'components': pca.components_,
            'features': features
        }
        
        # add principal components to the dataframe
        for i in range(len(features)):
            self.data['final'][f'PC{i+1}'] = X_pca[:, i]

# initialization
data_manager = DataManager()

# get_data for components
def get_data(stage='final'):
    return data_manager.data.get(stage)

def get_analysis_results():
    return data_manager.analysis_results