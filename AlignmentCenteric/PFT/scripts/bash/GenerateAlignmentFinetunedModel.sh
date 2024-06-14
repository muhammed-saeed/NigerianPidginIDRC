DATA_FILE=/PATH_TO/NPIDRC/align/awesomealign/rawData/english2pcmpostprocessing.txt
MODEL_NAME_OR_PATH="/PATH_TO/NPIDRC/align/awesomealign/finetunedmodels/finetuned"
OUTPUT_FILE=/PATH_TO/NPIDRC/align/awesomealign/rawData/english2pcmAlignmentFineTunedModelpostprocessedpidgin.txt
CUDA_VISIBLE_DEVICES=0 awesome-align \
    --output_file=$OUTPUT_FILE \
    --model_name_or_path=$MODEL_NAME_OR_PATH \
    --data_file=$DATA_FILE \
    --extraction 'softmax' \
    --batch_size 32