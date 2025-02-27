
from __future__ import print_function, division

import numpy as np
import sys

import nsfg
import thinkstats2

import warnings
warnings.filterwarnings('ignore')

from os.path import basename, exists
# Provides functions for working with file and directory paths in a way that is compatible across different operating systems.
# basename: Returns the final component of a path (e.g., the filename).
# exists: Checks if a path exists.

def download(url):
    """Defines a function 'download"""

    filename = basename(url) # Creates a variable that contains the filename of a provided url.
    if not exists(filename):
        # Checks if the file already exits, if not then the neccasary modules are imported the file is downloaded. Prints the name of the downloaded file.
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("Downloaded " + local)


def ReadFemResp(dct_file='2002FemResp.dct',
                dat_file='2002FemResp.dat.gz',
                nrows=None):
    """Reads the NSFG Respondent Data.
    
    dct_file: string file name
    dat_file: string file name
    
    Returns the a data frame from the data.
    """

    dct = thinkstats2.ReadStataDct(dct_file)
    df = dct.ReadFixedWidth(dat_file, compression='gzip', nrows=nrows)
    CleanFemResp(df)
    return df


def CleanFemResp(df):
    """Cleans data in given data frame."""
    pass

def ValidatePregnum(resp):
    """Validate pregnum in the respondent file.

    resp: respondent DataFrame
    """

    # Read through the pregnancy frame.
    preg = nsfg.ReadFemPreg()

    # Make the map from caseid to list of pregnancy indices.
    preg_map = nsfg.MakePregMap(preg)
    
    # Iterate through the respondent pregnum series
    for index, pregnum in resp.pregnum.items():
        caseid = resp.caseid[index]
        indices = preg_map[caseid]

        # Check that pregnum from the respondent file equals the number of records in the pregnancy file.
        if len(indices) != pregnum:
            print(caseid, len(indices), pregnum)
            return False

    return True


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    # Downloads
    download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemResp.dct")
    download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemResp.dat.gz")
    download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemPreg.dct")
    download("https://github.com/AllenDowney/ThinkStats2/raw/master/code/2002FemPreg.dat.gz")

    # Stores the df as resp.
    resp = ReadFemResp()

    # Checks for correct length.
    assert(len(resp) == 7643)
    # Checks for value count.
    assert(resp.pregnum.value_counts()[1] == 1267)
    # Checks for validation of Pregnum.
    assert(ValidatePregnum(resp))

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
