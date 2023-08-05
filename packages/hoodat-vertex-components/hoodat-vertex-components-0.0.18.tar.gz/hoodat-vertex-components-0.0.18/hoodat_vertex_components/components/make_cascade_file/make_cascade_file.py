import os
import argparse
import pandas as pd


def filter_cascades(cascade_ids):
    print(f"cascade_ids: {cascade_ids}")
    cascade_ids = [int(x) for x in cascade_ids]
    file_path = os.path.join(os.path.dirname(__file__), "cascades.csv")
    cascades = pd.read_csv(file_path)
    filtered_cascades = cascades[cascades["id"].isin(cascade_ids)]
    print(filtered_cascades)
    return filtered_cascades


def write_cascade_df(df, save_to_gcs: bool, output_filename: str):
    save_root = ""
    if save_to_gcs:
        save_root += "/gcs/"
    save_path = f"{save_root}{output_filename}"
    print(f"save_path: {save_path}")
    df.to_csv(save_path)
    return "Hey"


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--save_to_gcs",
        type=str2bool,
        help="Whether to save the file to gcs or not",
        default=False,
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        help="File to save cascades to",
        required=True,
    )
    parser.add_argument(
        "--cascade_ids",
        nargs="+",
        help="IDs to filter the cascade file down to",
        required=True,
    )
    args = parser.parse_args()
    df = filter_cascades(args.cascade_ids)
    write_cascade_df(
        df, save_to_gcs=args.save_to_gcs, output_filename=args.output_filename
    )
