# Super simple feature extraction pipeline

This is a super simple feature extraction pipeline for most kinds of images requiring feature extraction using SITK-readable images as input. It allows for the specification of patterns which filter images and masks using regular expressions, as well as the specification of patient/study identifiers in a similar manner and of a radiomics config file.

If co-registration/resampling of multimodal imaging is necessary please consult [this more complex pipeline](https://github.com/CCIG-Champalimaud/radiomics-pipeline).

## Usage

*Requires [`uv`](https://docs.astral.sh/uv/)*

```bash
uv run python -m src.extract_features \
    --input_folder /path/to/input/folder \
    --mask_folder /path/to/mask/folder \
    --identifier_pattern "(.+)" \
    --image_pattern "(.+)" \
    --mask_pattern "(.+)" \
    --config_path /path/to/config.yaml \
    --output_path /path/to/output.csv \
    --n_jobs 8
```

In `pipeline.sh`, a short script is provided to extract features for the GliomAI dataset.