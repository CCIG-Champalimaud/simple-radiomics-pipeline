import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Merge datasets.")

    parser.add_argument(
        "--input_csvs",
        type=Path,
        help="Input CSVs.",
        required=True,
        nargs="+",
    )
    parser.add_argument(
        "--suffixes",
        type=str,
        help="Suffixes.",
        required=True,
        nargs="+",
    )
    parser.add_argument(
        "--on",
        type=str,
        help="Column to merge on.",
        required=True,
        nargs="+",
    )
    parser.add_argument(
        "--output_path",
        type=Path,
        help="Output path.",
        required=True,
    )

    args = parser.parse_args()

    dfs = []
    assert len(args.input_csvs) == len(args.suffixes)
    for input_csv, suffix in zip(args.input_csvs, args.suffixes):
        df = pd.read_csv(input_csv).reset_index()
        df.columns = [
            col if col in args.on else col + "." + suffix for col in df.columns
        ]
        dfs.append(df)

    out_df = dfs[0]
    for df in dfs[1:]:
        out_df = pd.merge(out_df, df, on=args.on, how="outer")
    out_df.to_csv(args.output_path, index=False)
