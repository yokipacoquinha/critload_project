# ******************************************************
## Revision "$LastChangedDate: 2019-01-31 12:05:37 +0100 (Thu, 31 Jan 2019) $"
## Date "$LastChangedRevision: 620 $"
## Author "$LastChangedBy: arthurbeusen $"
## URL "$HeadURL: http://pbl.sliksvn.com/globalnutrients/aquaculture_allocation/trunk/tools/main_allocation.py $"
# ******************************************************
## ---------------------------------------------------------------------------
## -
## -    Name:    allocation.py
## -    Author:  Arthur Beusen PBL/IDM
## -    Date:    January 29 2019
## -    Purpose: Calculates the allocation of the freshwater aquaculture production.
## -
## ---------------------------------------------------------------------------


'''
Calculates the allocation of the freshwater aquaculture production
'''
# Python modules
import sys
import os
import traceback
import copy
import math
import optparse
import time

# Import Global ("generalcode") modules
import general_path

# Generalcode modules
import ascraster
from error import *
from iround import *

# Local modules
import general_startup
import temp_values
import groundwater
import surfacewater
import deposition
from print_debug import *


def run_critload_model(args):
    '''
    Main function to start the calculation of the critical load.
    '''

    # Parse command-line arguments and set parameters for script
    # Startup logging and runtime start
    params,log,s = general_startup.general_startup(args)

    # End reading arguments list of the commandline. Start the computation.


    # Set year and output directory
    year      = params.year
    outputdirname = params.outputdir
    print("YEAR: " + str(year))
    
    temp_values.temp_values(params)    
    
    print("RESULTS GROUNDWATER")
    groundwater.calculate(params)
    print("RESULTS SURFACE WATER")
    surfacewater.calculate(params)
    print("RESULTS DEPOSITION")
    deposition.calculate(params)
    
    log.write_and_print(s.total("Total run"))    
    del log

if (__name__ == "__main__"):
  
    try:
        # Start timer
        starttime_main = time.time()

        # Calculate the allocation
        run_critload_model(sys.argv)

        # End timer  
        endtime_main = time.time()
        print('Total simulation time (in s):  ' + str(endtime_main-starttime_main))
    except MyError as val:
        val.write()

    except (optparse.OptionValueError,
            ascraster.ASCIIGridError,
            Exception) as val:
        print(str(val))
        print(str(sys.exc_info()[0]))
        print(traceback.print_exc())
    except:
        print("***** ERROR ******")
        print("main_critload.py failed.")
        print(str(sys.exc_info()[0]))
        print(traceback.print_exc())    