export CODES=/PATH_TO/PLM4MT
export CKPT=/PATH_TO/PLM4MT/thump/mgpt
export MODEL_NAME=mgpt_msp
export OUTPUT_PATH=/PATH_TO/PLM4MT/checkpoints/PCM2En
export INPUT_FILE=/PATH_TO/PLM4MT/data/textFiles/BibleJw300TreeBankShuffled.pcm2en
export PYTHONPATH=$CODES:$PYTHONPATH

export USE_TF=0
export USE_TORCH=1

python -m torch.distributed.launch --nproc_per_node=3 --master_port=12345 $CODES/thumt/bin/trainer.py \
    --half \
    --input $INPUT_FILE \
    --output $OUTPUT_PATH \
    --model $MODEL_NAME \
    --ptm $CKPT \
    --hparam_set base \
    --distributed \
    --device_list=[1,2,3]

