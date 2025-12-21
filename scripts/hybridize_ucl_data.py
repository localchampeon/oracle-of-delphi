def hybridize(data):
    """
    this function takes a csv file - ucl data- for one year(2011) and create a whole
    new set of synthetic data for 2012. it then merges them and returns a full hybrid
    data set for 2 years.
    args:
    data = a csv file for UCL containing some part of 2010 and full 2011 trasctional data
    """
    import pandas as pd
    from datetime import datetime as dt
    import numpy as np

    #copy data and drop 2010 rows
    data.columns = data.columns.str.lower()
    data_synth = data.copy()
    data_synth['year'] = data_synth['invoicedate'].dt.year
    data_synth = data_synth[data_synth['year'] == 2011]
    data_synth.drop('year',axis=1, inplace = True)
    data_synth.head()
    
    #create synthetic data for invoice date: one year
    data_synth['invoicedate'] = pd.to_datetime(data_synth['invoicedate'] + pd.DateOffset(years =1))

    #Introduce realistic volume variation 15+ to -15 variations introduced
    scale_factor = np.random.uniform(0.85, 1.15, len(data_synth))
    data_synth['quantity'] = (data_synth['quantity'] * scale_factor).round().astype(int)

    #introduce synthetic missingness by adding 2% missing values to the data
    mask = np.random.rand(len(data_synth)) < 0.02 # rand generates values btw 0 and 1. 0.02 is 2% equiv
    data_synth['customerid'] = data_synth.loc[mask, 'customerid'] = None #"Keep only the rows where the mask is True."

    data_synth['sales_channel'] = np.random.choice(
    ['online','offline'], size = len(data_synth), p = [0.7,0.3]
    )

    #merge the 2 cells
    data_hybrid = pd.concat([data,data_synth], ignore_index=True)

    #calculate revenue
    data_hybrid['revenue'] = data_hybrid['quantity'] * data_hybrid['unitprice']

    data_hybrid.to_csv('sales_hybrid_data.csv',index = False)

    return
