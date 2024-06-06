TRAIN_FILE=/local/musaeed/NPIDRC/align/PFT/English2PidingTrain.txt
EVAL_FILE=/local/musaeed/NPIDRC/align/PFT/English2PidingDev.txt
OUTPUT_DIR=/local/musaeed/NPIDRC/align/PFT/finetunedmodels/finetunedTreebankModel
CUDA_VISIBLE_DEVICES=2 awesome-train \
    --output_dir=$OUTPUT_DIR \
    --model_name_or_path=bert-base-multilingual-cased \
    --extraction 'softmax' \
    --do_train \
    --train_mlm \
    --train_tlm \
    --train_tlm_full \
    --train_so \
    --train_psi \
    --train_data_file=$TRAIN_FILE \
    --per_gpu_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --num_train_epochs 1 \
    --learning_rate 2e-5 \
    --save_steps 10000 \
    --max_steps 40000 \
    --do_eval \
    --eval_data_file=$EVAL_FILE