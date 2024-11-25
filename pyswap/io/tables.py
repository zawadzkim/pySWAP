import io
import pandas as pd

def string_to_dataframe(df_string):
    # Remove any leading/trailing whitespace and split into lines
    lines = df_string.strip().split('\n')
    
    # Extract the header
    header = lines[0].split()
    
    # Create a StringIO object with the data (excluding the header)
    data = io.StringIO('\n'.join(lines[1:]))
    
    # Read the fixed-width formatted data
    df = pd.read_fwf(data, header=None, names=header)
    
    return df