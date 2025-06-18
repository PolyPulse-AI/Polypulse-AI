import requests
import pandas as pd
from datetime import datetime
import uuid

# Placeholder for Polymarket API or scraper endpoint
POLYMARKET_API_URL = "https://api.polymarket.com/markets"  # Replace with actual API or scraper endpoint

def fetch_polymarket_data():
    """
    Fetch market data from Polymarket API or scraper.
    Returns a list of markets with details like name, outcomes, prices, volume, liquidity.
    """
    try:
        # Example API call (replace with actual Polymarket API or scraper logic)
        response = requests.get(POLYMARKET_API_URL)
        response.raise_for_status()
        markets = response.json()
        return markets
    except Exception as e:
        print(f"Error fetching data: {e}")
        # Fallback: Mock data for demonstration
        return [
            {
                "id": str(uuid.uuid4()),
                "title": "Will Bitcoin exceed $100,000 by Dec 2025?",
                "outcomes": ["Yes", "No"],
                "prices": [0.65, 0.35],
                "volume": 500000,  # USDC
                "liquidity": 100000,  # USDC
                "end_date": "2025-12-31",
                "category": "Crypto"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Who will win the 2026 World Cup?",
                "outcomes": ["Brazil", "France", "Argentina", "Other"],
                "prices": [0.30, 0.25, 0.20, 0.25],
                "volume": 200000,
                "liquidity": 50000,
                "end_date": "2026-07-15",
                "category": "Sports"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Will TikTok be banned in the US in 2025?",
                "outcomes": ["Yes", "No"],
                "prices": [0.45, 0.55],
                "volume": 300000,
                "liquidity": 80000,
                "end_date": "2025-12-31",
                "category": "Politics"
            }
        ]

def analyze_markets(markets):
    """
    Analyze markets based on liquidity, volume, and price discrepancy.
    Returns a DataFrame with scores and recommendations.
    """
    # Convert to DataFrame
    df = pd.DataFrame(markets)
    
    # Calculate metrics
    df['total_volume'] = df['volume']
    df['liquidity_score'] = df['liquidity'] / df['liquidity'].max()  # Normalize liquidity
    df['volume_score'] = df['total_volume'] / df['total_volume'].max()  # Normalize volume
    
    # Price discrepancy: Check if sum of prices deviates from 1 (arbitrage opportunity)
    df['price_sum'] = df['prices'].apply(sum)
    df['arbitrage_opportunity'] = abs(df['price_sum'] - 1.0)
    
    # Time to expiration (days remaining)
    df['days_to_end'] = df['end_date'].apply(
        lambda x: (datetime.strptime(x, '%Y-%m-%d') - datetime.now()).days
    )
    
    # Score markets (weighted combination of metrics)
    df['score'] = (
        0.4 * df['liquidity_score'] +  # Prioritize liquidity
        0.3 * df['volume_score'] +     # Consider trading activity
        0.2 * df['arbitrage_opportunity'] * 10 +  # Amplify arbitrage impact
        0.1 * (1 / (df['days_to_end'] + 1))  # Favor near-term markets
    )
    
    # Rank markets
    df = df.sort_values(by='score', ascending=False)
    
    return df[['id', 'title', 'category', 'prices', 'total_volume', 'liquidity', 'end_date', 'score', 'arbitrage_opportunity']]

def generate_report(df):
    """
    Generate a markdown report of recommended markets.
    Returns a string with the report content.
    """
    report = "# Polymarket Analyzer Report\n\n"
    report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += "## Top Markets to Enter\n\n"
    
    for _, row in df.head(5).iterrows():
        report += f"### {row['title']}\n"
        report += f"- **Category**: {row['category']}\n"
        report += f"- **Outcomes and Prices**: {', '.join([f'{o}: ${p}' for o, p in zip(row['outcomes'], row['prices'])] if 'outcomes' in row else 'N/A')}\n"
        report += f"- **Volume**: ${row['total_volume']:,.2f} USDC\n"
        report += f"- **Liquidity**: ${row['liquidity']:,.2f} USDC\n"
        report += f"- **End Date**: {row['end_date']}\n"
        report += f"- **Score**: {row['score']:.3f}\n"
        report += f"- **Arbitrage Opportunity**: {row['arbitrage_opportunity']:.3f}\n"
        report += "\n"
    
    return report

def main():
    # Fetch market data
    markets = fetch_polymarket_data()
    
    # Analyze markets
    analyzed_df = analyze_markets(markets)
    
    # Generate report
    report = generate_report(analyzed_df)
    
    # Save report to file
    with open("polymarket_report.md", "w") as f:
        f.write(report)
    
    print("Analysis complete. Report saved as 'polymarket_report.md'.")

if __name__ == "__main__":
    main()