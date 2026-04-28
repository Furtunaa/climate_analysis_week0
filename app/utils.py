# app/utils.py
import pandas as pd
import numpy as np
import os

COUNTRIES = ['Ethiopia', 'Kenya', 'Sudan', 'Tanzania', 'Nigeria']
COLORS = {
    'Ethiopia': '#E45756',
    'Kenya': '#4C9BE8',
    'Sudan': '#F5A623',
    'Tanzania': '#7ED321',
    'Nigeria': '#9B59B6',
}
VARIABLE_LABELS = {
    'T2M': 'Temperature at 2m (°C)',
    'T2M_MAX': 'Maximum Temperature (°C)',
    'T2M_MIN': 'Minimum Temperature (°C)',
    'PRECTOTCORR': 'Precipitation (mm/day)',
    'RH2M': 'Relative Humidity (%)',
    'WS2M': 'Wind Speed (m/s)',
}

def load_all_countries():
    """Load all cleaned CSV files from data/ directory"""
    all_dfs = []
    data_dir = 'data'
    
    for country in COUNTRIES:
        file_path = f'{data_dir}/{country.lower()}_clean.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, parse_dates=['Date'])
            df['Country'] = country
            df['Year'] = df['Date'].dt.year
            all_dfs.append(df)
            print(f'Loaded {country}: {len(df)} rows')
    
    if not all_dfs:
        return pd.DataFrame()
    
    return pd.concat(all_dfs, ignore_index=True)

def filter_data(df, countries, year_range):
    """Filter by selected countries and year range"""
    mask = (df['Country'].isin(countries)) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
    return df[mask].copy()

def compute_monthly_avg(df, variable):
    """Compute monthly averages per country"""
    monthly = df.groupby(['Country', pd.Grouper(key='Date', freq='ME')])[variable].mean().reset_index()
    return monthly.dropna()

def compute_annual_extreme_heat(df, threshold=35):
    """Count days per year with temperature above threshold"""
    if 'T2M_MAX' not in df.columns:
        return pd.DataFrame()
    heat = df[df['T2M_MAX'] > threshold].groupby(['Country', 'Year']).size().reset_index(name='Days')
    return heat

def compute_vulnerability_scores(df):
    """Compute composite vulnerability ranking"""
    scores = {}
    for country in df['Country'].unique():
        cdf = df[df['Country'] == country]
        scores[country] = {
            'Mean T2M (°C)': cdf['T2M'].mean(),
            'Precip Std Dev': cdf['PRECTOTCORR'].std(),
            'Extreme Heat Days': (cdf['T2M_MAX'] > 35).sum(),
            'Dry Days (%)': (cdf['PRECTOTCORR'] < 1).mean() * 100,
        }
    
    vuln_df = pd.DataFrame(scores).T
    
    # Normalize and compute composite
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    normalized = pd.DataFrame(
        scaler.fit_transform(vuln_df),
        index=vuln_df.index,
        columns=vuln_df.columns
    )
    normalized['Composite Score'] = normalized.sum(axis=1)
    
    # Add rank
    result = normalized[['Composite Score']].sort_values('Composite Score', ascending=False)
    result['Rank'] = range(1, len(result) + 1)
    
    return result