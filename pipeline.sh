ROOT_FOLDER=/mnt/big_disk/data/glioma
OUTPUT_FOLDER=statistics
N_JOBS=32

for tp_id in preop postop
do
    if [ $tp_id == "preop" ]; then
        INPUT_FOLDER=$ROOT_FOLDER/preop_scans
        MASK_FOLDER=$ROOT_FOLDER/preop_masks_v2
    else
        INPUT_FOLDER=$ROOT_FOLDER/gliomai_postoperative
        MASK_FOLDER=$ROOT_FOLDER/gliomai_postop_masks
    fi
    for image in brain_t1c brain_t1n brain_t2w brain_t2f
    do 
        out_path=$OUTPUT_FOLDER/statistics/$tp_id.$image.csv
        if [ -f $out_path ]; then
            echo "Statistics already calculated for $tp_id $image"
            continue
        fi
        uv run python \
            -m src.extract_statistics \
            --input_folder $INPUT_FOLDER \
            --identifier_pattern '(?<=/)[0-9]+(?=/)' \
            --image_pattern ".*$image.*" \
            --output_path $OUTPUT_FOLDER/statistics/$tp_id.$image.csv
    done

    for image in brain_t1c brain_t1n brain_t2w brain_t2f
    do 
        out_path=$OUTPUT_FOLDER/features/$tp_id.$image.csv
        if [ -f $out_path ]; then
            echo "Features already calculated for $tp_id $image"
            continue
        fi
        uv run python \
            -m src.extract_features \
            --input_folder $INPUT_FOLDER \
            --mask_folder $MASK_FOLDER  \
            --identifier_pattern '(?<=/)[0-9]+(?=/)' \
            --image_pattern ".*$image.*" \
            --mask_pattern '.*tumor_mask.*' \
            --config_path radiomics/radiomicsConfig.yaml  \
            --output_path $OUTPUT_FOLDER/features/$tp_id.$image.csv \
            --n_jobs $N_JOBS
    done
done