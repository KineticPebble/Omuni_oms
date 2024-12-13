import pandas as pd

def fill_null(df: list) -> list:
    '''coneverts empty string to None from the data

    Parameters:
        df: 2 dimentional list containing tabular data

    Returns:
        modified list
    '''
    print("filling NULL")
    for l in range(len(df)):
        df[l] = [x if x != '' else None for x in df[l]]
    return df

def fill_NaT(df: list) -> list:
    '''converts NaT datatype to None from the data

    Parameters:
        df: 2 dimentional list containing tabular data

    Returns:
        modified list
    '''
    print("filling_NaT")
    for l in range(len(df)):
        df[l] = [x if type(x) != pd._libs.tslibs.nattype.NaTType else None for x in df[l]]
    return df
