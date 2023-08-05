import os
import argparse
import pandas as pd


def filter_cascades(ids):
    print(ids)
    file_path = os.path.join(os.path.dirname(__file__), "cascades.csv")
    cascades = pd.read_csv(file_path)
    filtered_cascades = cascades[cascades["id"].isin(ids)]
    print(filtered_cascades)
    return filtered_cascades


def write_file():
    return "Hey"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ids",
        type=int,
        nargs="+",
        help="IDs to filter the cascade file down to",
        required=True,
    )
    args = parser.parse_args()
    filter_cascades(args.ids)
