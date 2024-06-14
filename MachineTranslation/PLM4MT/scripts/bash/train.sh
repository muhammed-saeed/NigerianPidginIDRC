CODES=/PATH_TO/PLM4MT
CKPT=/PATH_TO/PLM4MT/checkpoints/thump/mgpt
MODEL_NAME=mgpt_msp
OUTPUT_PATH=/PATH_TO/PLM4MT/checkpoints/PCM2En
INPUT_FILE=/PATH_TO/PLM4MT/data/textFiles/BibleJw300TreeBankShuffled.pcm2en
export PYTHONPATH=$CODES:$PYTHONPATH

export USE_TF=0
export USE_TORCH=1

python3 $CODES/thumt/bin/trainer.py \
    --half \
    --input $INPUT_FILE \
    --model $MODEL_NAME \
    --ptm $CKPT \
    --hparam_set base

#    --parameters="device_list=[3,4,5] train_steps=40000 update_cycle=16 batch_size=256 save_checkpoint_steps=2000 max_length=256" \
