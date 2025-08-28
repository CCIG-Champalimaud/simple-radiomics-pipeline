import pandas as pd
import SimpleITK as sitk
from tqdm import tqdm
from pathlib import Path
from .extract_features import get_image_dict


def calculate_statistics(
    input_folder: Path, identifier_pattern: Path, image_pattern: Path
) -> pd.DataFrame:
    image_dict = get_image_dict(input_folder, identifier_pattern, image_pattern)

    all_values = {}

    for identifier, images in tqdm(image_dict.items()):
        for image_path in images:
            mmf = sitk.MinimumMaximumImageFilter()
            image = sitk.ReadImage(image_path)
            mmf.Execute(image)
            k = identifier + "_" + str(image_path.name)
            all_values[k] = {
                "min": mmf.GetMinimum(),
                "max": mmf.GetMaximum(),
                "shape": image.GetSize(),
                "spacing": image.GetSpacing(),
            }
            print(f"{k} - {all_values[k]}")

    df = pd.DataFrame(all_values).T

    df.sort_values(by=["min", "max"], ascending=[True, True], inplace=True)

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract statistics.")

    parser.add_argument(
        "--input_folder",
        type=Path,
        help="Input folder.",
        required=True,
    )
    parser.add_argument(
        "--identifier_pattern",
        type=str,
        help="Identifier pattern.",
        required=True,
    )
    parser.add_argument(
        "--image_pattern",
        type=str,
        help="Image pattern.",
        required=True,
    )
    parser.add_argument(
        "--output_path",
        type=Path,
        help="Output path.",
    )

    args = parser.parse_args()

    df = calculate_statistics(
        args.input_folder, args.identifier_pattern, args.image_pattern
    )

    if args.output_path is not None:
        args.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output_path)
