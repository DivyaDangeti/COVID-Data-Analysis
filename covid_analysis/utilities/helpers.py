import logging
import os
import datetime
import requests
import pandas as pd


logger = logging.getLogger("__main__.helpers")

# Log function is used to declare a logger object which 
# creates a log file and also prints the same on your log console for debugging.
def log(loggerName, filename, logfolder="logs"):
    """
    function description:
        This function is used to declare a logger obeject,
        which would create a log file in logs path
    Inputs: loggerName and filename for the log
    Output: logger object
    """

    # date method
    dt = datetime.datetime.now()

    # Create a custom logger
    logger = logging.getLogger(loggerName)

    # Create log folder if not exists

    if not os.path.exists(logfolder):
        print("Creating logs folder as it not exists....")
        os.mkdir(logfolder)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(
        os.path.join(logfolder, filename + "_" + dt.strftime("%Y%m%d") + ".log")
    )
    logger.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s"
    )
    c_handler.setFormatter(format)
    f_handler.setFormatter(format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


def reading_url(url, data_type="csv"):
    try:
        response = requests.get(url, verify=True)
        response.raise_for_status()

        if data_type.lower() == "csv":
            data = response.text
        elif data_type.lower() == "json":
            data = response.json()
        else:
            logger.error("reading_url didn't got the expected data_type")
            raise Exception("Provided datatype is not in allowed list for reading_url")

        logger.info(f"url response was successful with code: {response.status_code}")
        return data

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

def subtract_days_from_date(date, days):
    """Subtract days from a date and return the date.
    
    Args: 
        date (string): Date string in YYYY-MM-DD format. 
        days (int): Number of days to subtract from date
    
    Returns: 
        date (date): Date in YYYY-MM-DD with X days subtracted. 
    """
    
    subtracted_date = pd.to_datetime(date) - pd.to_timedelta(days, unit='d')
    subtracted_date = subtracted_date.strftime("%Y-%m-%d")

    return subtracted_date