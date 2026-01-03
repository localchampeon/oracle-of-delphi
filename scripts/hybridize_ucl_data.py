#deep seek
import pandas as pd
import numpy as np

def hybridize(data, seed=42):
    """
    Create hybrid 2011 (real) + 2012 (synthetic) sales data
    from UCI Online Retail dataset.
    """
    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Standardize columns
    data.columns = data.columns.str.lower()
    
    # Convert date
    data['invoicedate'] = pd.to_datetime(data['invoicedate'])
    
    # Get 2011 data only
    data_2011 = data[data['invoicedate'].dt.year == 2011].copy()
    
    # Create 2012 synthetic data
    data_2012 = data_2011.copy()
    
    # Shift dates by 1 year + random variation (±2 days)
    date_variation = pd.to_timedelta(np.random.randint(-2, 3, len(data_2012)), unit='D')
    data_2012['invoicedate'] = data_2012['invoicedate'] + pd.DateOffset(years=1) + date_variation
    
    # Make invoice numbers unique
    data_2012['invoiceno'] = data_2012['invoiceno'].astype(str) + 'S'
    
    # Scale quantities (product-specific patterns)
    if 'stockcode' in data_2012.columns:
        product_groups = data_2012['stockcode'].astype('category').cat.codes % 3
    else:
        product_groups = np.random.randint(0, 3, len(data_2012))
    
    scale_factors = np.where(
        product_groups == 0, np.random.uniform(0.9, 1.1, len(data_2012)),
        np.where(
            product_groups == 1, np.random.uniform(1.1, 1.3, len(data_2012)),
            np.random.uniform(0.7, 0.9, len(data_2012))
        )
    )
    
    data_2012['quantity'] = (data_2012['quantity'] * scale_factors).round().astype(int)
    data_2012['quantity'] = data_2012['quantity'].clip(lower=1)
    
    # Adjust prices for 2012
    price_adjust = np.where(
        product_groups == 1, np.random.uniform(1.05, 1.15, len(data_2012)),
        np.random.uniform(1.02, 1.04, len(data_2012))
    )
    data_2012['unitprice'] = (data_2012['unitprice'] * price_adjust).round(2)
    
    # FIXED: Nullify 2% of customer IDs - use simple random method
    if 'customerid' in data_2012.columns:
        mask = np.random.rand(len(data_2012)) < 0.02
        data_2012.loc[mask, 'customerid'] = np.nan
    
    # Sales channels
    data_2011['sales_channel'] = 'online'
    data_2012['sales_channel'] = np.random.choice(
        ['online', 'offline'], 
        size=len(data_2012), 
        p=[0.8, 0.2]
    )
    
    # Combine datasets
    hybrid_data = pd.concat([data_2011, data_2012], ignore_index=True)
    
    # Calculate revenue
    hybrid_data['revenue'] = (hybrid_data['quantity'] * hybrid_data['unitprice']).round(2)
    
    # Handle negative quantities
    if (hybrid_data['quantity'] < 0).any():
        neg_count = (hybrid_data['quantity'] < 0).sum()
        print(f"Note: Found {neg_count} negative quantities - converting to positive")
        hybrid_data.loc[hybrid_data['quantity'] < 0, 'quantity'] = hybrid_data.loc[hybrid_data['quantity'] < 0, 'quantity'].abs()
        hybrid_data.loc[hybrid_data['quantity'] < 0, 'revenue'] = hybrid_data.loc[hybrid_data['quantity'] < 0, 'revenue'] * -1
    
    # Save
    hybrid_data.to_csv('hybrid_sales_data_deepseek.csv', index=False)
    
    # Summary
    print("=" * 50)
    print("HYBRID DATA CREATED SUCCESSFULLY")
    print("=" * 50)
    print(f"Total records: {len(hybrid_data):,}")
    print(f"  2011 (real): {len(data_2011):,}")
    print(f"  2012 (synth): {len(data_2012):,}")
    print(f"Date range: {hybrid_data['invoicedate'].min().date()} to {hybrid_data['invoicedate'].max().date()}")
    print(f"Total revenue: ${hybrid_data['revenue'].sum():,.2f}")
    print(f"File saved: hybrid_sales_data.csv")
    print("=" * 50)
    
    return hybrid_data


# Usage
if __name__ == "__main__":
    # Load your data
    data = pd.read_excel("C:/Users/Lenovo/Documents/MerchantOfVenice/ucl_data.xlsx")
    
    # Create hybrid dataset
    df = hybridize(data, seed=42)
    
    # Show first few rows
    print("\nFirst 5 rows:")
    print(df.head())
