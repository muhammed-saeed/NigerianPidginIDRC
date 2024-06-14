CODES=/PATH_TO/PLM4MT
export PYTHONPATH=/PATH_TO/PLM4MT:$PYTHONPATH

python $CODES/thumt/bin/translator.py \
  --input /PATH_TO/PLM4MT/data/textFiles/decoding.txt \
  --ptm /PATH_TO/PLM4MT/checkpoints/thump/mgpt \
  --output "/PATH_TO/PLM4MT/data/textFiles/decodingoutput.txt" \
  --model mgpt_msp \
  --half --prefix "/PATH_TO/PLM4MT/train/model-6.pt" \
 