# ***********************************************************************
# Name:  covid_analysis.py
#
# Description:  This module will be the main module for our project
# "COVID DATA ANALYSIS"
#
#
# Dependencies: requirements.txt
#
# Revision History
#
# 9/7/21	DD		Origin
# 12/2/21   Project Demo
# ***********************************************************************

import os
from pathlib import Path
import utilities.helpers as helper

path = Path(__file__)
logger = helper.log(__name__, os.path.basename(path.with_suffix("")))
import utilities.plotly_dash as plt_dash


if __name__ == "__main__":
    try:
        logger.info("Step-0 Preparing your app")
        plt_dash.app.run_server(debug=False)

    except Exception as e:
        logger.exception(f"Process failed with exception: '{e}'")
