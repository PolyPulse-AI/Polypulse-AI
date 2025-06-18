import pytest
import pandas as pd
from polymarket_analyzer import fetch_polymarket_data, analyze_markets

def test_fetch_polymarket_data():
    """Test that fetch_polymarket_data returns a list of markets."""
    markets = fetch_polymarket_data()
    assert isinstance(markets, list)
    assert len(markets) > 0
    assert "title" in markets[0]
    assert "prices" in markets[0]

def test_analyze_markets():
    """Test that analyze_markets returns a sorted DataFrame with scores."""
    markets = [
        {
            "id": "1",
            "title": "Test Market 1",
            "outcomes": ["Yes", "No"],
            "prices": [0.6, 0.4],
            "volume": 100000,
            "liquidity": 50000,
            "end_date": "2025-12-31",
            "category": "Test"
        }
    ]
    df = analyze_markets(markets)
    assert isinstance(df, pd.DataFrame)
    assert "score" in df.columns
    assert df["score"].iloc[0] > 0