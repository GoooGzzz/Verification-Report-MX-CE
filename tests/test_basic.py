"""
Basic tests for the Samsung Field Intelligence Dashboard
"""
import pytest
import pandas as pd
from io import BytesIO

from app.config import REQUIRED_COLUMNS
from app.data_processing import calculate_kpis

def test_calculate_kpis():
    """Test KPI calculation with sample data"""
    # Create sample data
    sample_data = pd.DataFrame({
        'W': [1, 1, 1],
        'Shop Code': ['S001', 'S001', 'S002'],
        'Shop Name': ['Store 1', 'Store 1', 'Store 2'],
        'Brand': ['Samsung', 'Samsung', 'Other'],
        'Model': ['A1', 'A2', 'B1'],
        'Sellout': [100, 150, 200],
        'Shelf Share': [30.0, 25.0, 45.0],
        'Price': [500, 600, 400],
        'Project': ['P1', 'P1', 'P1'],
        'Category': ['Phone', 'Phone', 'Phone'],
        'Price segmentation': ['High', 'High', 'Mid']
    })

    kpis = calculate_kpis(sample_data)

    assert kpis['total_shops'] == 2
    assert kpis['sam_sellout'] == 250  # 100 + 150
    assert kpis['total_sellout'] == 450  # 100 + 150 + 200
    assert kpis['sam_share_pct'] == pytest.approx(55.56, rel=1e-2)  # 250/450 * 100
    assert kpis['total_records'] == 3

def test_required_columns():
    """Test that required columns are properly defined"""
    assert 'W' in REQUIRED_COLUMNS
    assert 'Shop Code' in REQUIRED_COLUMNS
    assert 'Brand' in REQUIRED_COLUMNS
    assert len(REQUIRED_COLUMNS) == 11

if __name__ == "__main__":
    pytest.main([__file__])