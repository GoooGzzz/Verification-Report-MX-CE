"""
Data processing and analysis functions for the dashboard
"""
import pandas as pd
import streamlit as st
from typing import Tuple, Optional, Dict, Any
from app.config import REQUIRED_COLUMNS

@st.cache_data
def load_data(file) -> pd.DataFrame:
    """
    Load and validate Excel data file

    Args:
        file: Uploaded file object

    Returns:
        pd.DataFrame: Processed dataframe

    Raises:
        ValueError: If required columns are missing or data is invalid
    """
    try:
        df = pd.read_excel(file)
        df.columns = df.columns.str.strip()

        # Check for required columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        # Convert numeric columns
        for col in ['Sellout', 'Shelf Share', 'Price']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Add computed columns
        df['is_samsung'] = df['Brand'] == 'Samsung'

        return df

    except Exception as e:
        raise ValueError(f"Error loading Excel file: {str(e)}")

@st.cache_data
def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect data anomalies and quality issues

    Args:
        df: Input dataframe

    Returns:
        pd.DataFrame: Anomalies dataframe
    """
    try:
        flags = []

        # Single-model 100% shelf share
        if 'Shelf Share' in df.columns:
            ss100 = df[df['Shelf Share'] == 100][[
                'W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share'
            ]].copy()
            if len(ss100) > 0:
                ss100['Issue'] = '🔴 Shelf Share = 100% (impossible single model)'
                ss100['Severity'] = 'HIGH'
                flags.append(ss100)

        # Brand shelf total > 100%
        if all(col in df.columns for col in ['W', 'Shop Code', 'Brand', 'Shelf Share']):
            shelf_total = df.groupby(['W', 'Shop Code', 'Brand'])['Shelf Share'].sum().reset_index()
            shelf_total.columns = ['W', 'Shop Code', 'Brand', 'Total_SS']
            over100 = shelf_total[shelf_total['Total_SS'] > 100].merge(
                df[['Shop Code', 'Shop Name']].drop_duplicates(), on='Shop Code', how='left')
            if len(over100) > 0:
                over100['Model'] = '—'
                over100['Shelf Share'] = over100['Total_SS']
                over100['Issue'] = over100['Total_SS'].apply(
                    lambda x: f'🟠 Brand shelf share total = {x:.0f}% (exceeds 100%)')
                over100['Severity'] = 'MEDIUM'
                flags.append(over100[[
                    'W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share', 'Issue', 'Severity'
                ]])

        # Statistical sellout outliers
        if 'Sellout' in df.columns:
            mean_s, std_s = df['Sellout'].mean(), df['Sellout'].std()
            if std_s > 0:
                high_sell = df[df['Sellout'] > mean_s + 3 * std_s][[
                    'W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Sellout'
                ]].copy()
                if len(high_sell) > 0:
                    high_sell = high_sell.rename(columns={'Sellout': 'Shelf Share'})
                    high_sell['Issue'] = high_sell['Shelf Share'].apply(
                        lambda x: f'🟡 Sellout = {x:.0f} units (statistical outlier)')
                    high_sell['Severity'] = 'MEDIUM'
                    flags.append(high_sell[[
                        'W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share', 'Issue', 'Severity'
                    ]])

        # Combine all flags
        valid = [f for f in flags if len(f) > 0]
        return pd.concat(valid, ignore_index=True) if valid else pd.DataFrame(
            columns=['W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share', 'Issue', 'Severity'])

    except Exception as e:
        st.warning(f"Error detecting anomalies: {str(e)}")
        return pd.DataFrame(columns=[
            'W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share', 'Issue', 'Severity'
        ])

@st.cache_data
def build_store_agg(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build store-level aggregations

    Args:
        df: Filtered dataframe

    Returns:
        pd.DataFrame: Store aggregations
    """
    try:
        required_cols = ['Shop Code', 'Shop Name', 'Project', 'Sellout', 'Shelf Share', 'Brand']
        if not all(col in df.columns for col in required_cols):
            return pd.DataFrame()

        sa = df.groupby(['Shop Code', 'Shop Name', 'Project']).agg(
            Total_Sellout=('Sellout', 'sum'),
            Sam_Sellout=('Sellout', lambda x: x[df.loc[x.index, 'Brand'] == 'Samsung'].sum()),
            Sam_Shelf=('Shelf Share', lambda x: x[df.loc[x.index, 'Brand'] == 'Samsung'].mean()),
            Brands_Stocked=('Brand', 'nunique'),
            Models_Stocked=('Model', 'nunique'),
        ).reset_index()

        sa['Sam_Sellout'] = sa['Sam_Sellout'].fillna(0)
        sa['Sam_Share_Pct'] = (sa['Sam_Sellout'] / sa['Total_Sellout'] * 100).round(1).fillna(0)
        sa['Sam_Shelf'] = sa['Sam_Shelf'].fillna(0).round(1)

        return sa

    except Exception as e:
        st.warning(f"Error building store aggregates: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def build_wow_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build week-over-week alerts

    Args:
        df: Input dataframe

    Returns:
        pd.DataFrame: WoW alerts
    """
    try:
        if 'W' not in df.columns or 'Sellout' not in df.columns or 'Shop Code' not in df.columns:
            return pd.DataFrame()

        weekly = df[df['Brand'] == 'Samsung'].groupby(['W', 'Shop Code', 'Shop Name'])['Sellout'].sum().reset_index()
        weeks = sorted(weekly['W'].unique())

        if len(weeks) < 2:
            return pd.DataFrame()

        alerts = []
        for i in range(1, len(weeks)):
            prev = weekly[weekly['W'] == weeks[i - 1]][[
                'Shop Code', 'Shop Name', 'Sellout'
            ]].rename(columns={'Sellout': 'Prev'})
            curr = weekly[weekly['W'] == weeks[i]][[
                'Shop Code', 'Shop Name', 'Sellout'
            ]].rename(columns={'Sellout': 'Curr'})

            m = prev.merge(curr, on=['Shop Code', 'Shop Name'], how='outer').fillna(0)
            m['Change_Pct'] = ((m['Curr'] - m['Prev']) / m['Prev'].replace(0, 1) * 100).round(1)
            m['From_Week'] = weeks[i - 1]
            m['To_Week'] = weeks[i]
            alerts.append(m)

        return pd.concat(alerts, ignore_index=True) if alerts else pd.DataFrame()

    except Exception as e:
        st.warning(f"Error building WoW alerts: {str(e)}")
        return pd.DataFrame()

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate key performance indicators

    Args:
        df: Filtered dataframe

    Returns:
        Dict containing KPI values
    """
    try:
        sam_df = df[df['Brand'] == 'Samsung']
        total_sellout = df['Sellout'].sum()
        sam_sellout = sam_df['Sellout'].sum()

        return {
            'total_shops': df['Shop Code'].nunique(),
            'sam_sellout': sam_sellout,
            'total_sellout': total_sellout,
            'sam_share_pct': (sam_sellout / total_sellout * 100) if total_sellout > 0 else 0,
            'sam_avg_shelf': sam_df['Shelf Share'].mean() if len(sam_df) > 0 else 0,
            'total_records': len(df),
            'weeks_analyzed': df['W'].nunique(),
            'brands_tracked': df['Brand'].nunique(),
            'categories': df['Category'].nunique(),
            'price_segments': df['Price segmentation'].nunique()
        }

    except Exception as e:
        st.error(f"Error calculating KPIs: {str(e)}")
        return {
            'total_shops': 0,
            'sam_sellout': 0,
            'total_sellout': 0,
            'sam_share_pct': 0,
            'sam_avg_shelf': 0,
            'total_records': 0,
            'weeks_analyzed': 0,
            'brands_tracked': 0,
            'categories': 0,
            'price_segments': 0
        }