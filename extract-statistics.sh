for image in brain_t1c brain_t1n brain_t2w brain_t2f
do 
    uv run python \
        -m src.extract_statistics \
        --input_folder /mnt/big_disk/data/glioma/gliomai_postoperative \
        --identifier_pattern '[0-9]+' \
        --image_pattern ".*$image.*" \
        --output_path statistics/gliomai_postoperative_$image.csv
done