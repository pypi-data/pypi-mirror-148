import logging
from npd_cat_corr.data_construction import create_dataset
import argparse
import pandas as pd
import os


def main():

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(prog="get-correlation-data", description="Script to create full category correlations dataset. Must have Bloomberg Terminal running.")

    parser.add_argument("ewPath", type=input_path, help="Path to latest EquityWatch flat file")
    parser.add_argument("outputPath", type=output_path, nargs="?", default="./correlation_data.csv", help="Output path for final product")

    args = parser.parse_args()

    try:
        ew_df = pd.read_csv(args.ewPath)
    except:
        logging.error("Invalid Equity Watch file or path")
        return

    try:
        corr_data = create_dataset(ew_df, log=True)
    except Exception as e:
        logging.error("Internal Package error: {e}".format(e=str(e)))
        return

    corr_data.to_csv(args.outputPath, index=False)
    
    
def input_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid filepath")

def output_path(path):

    if os.path.isdir(path):
        if path[-1] == "/":
            return path + "correlation_data.csv"
        else:
            return path + "/correlation_data.csv"
    elif path.endswith(".csv"):
        ind = path.rfind("/")
        if ind == -1:
            return "./" + path
        elif os.path.isdir(path[:ind]):
            return path
        else:
            raise argparse.ArgumentTypeError(f"{path} is not a valid filepath")
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid filepath") 


