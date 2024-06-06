
CUDA_VISIBLE_DEVICES=6 python /local/musaeed/DiscoPrompt/DiscoPromptPidginContinueFromCheckpoint.py \
--template_id 0 --max_steps 30000 \
--csv_file_path "/local/musaeed/NPIDRC/FullTransferMethod/Implicit/dataset/ProjectedDataSet/Merged&Processed/pft/pdtb2PidginImplicitEntrel.csv" \
--batch_size 4 --eval_every_steps 250 \
--dataset ji --model_name_or_path google/t5-v1_1-large \
--result_file /local/musaeed/NPIDRC/FullTransferMethod/Results/DiscoPrompt/Scratch/PFT/t5_v1_1_large/03LearningRateDiscoPromptClassification_PDTB2Scratch.txt \
--ckpt_file FullTransferCheckpoints/PFT/Scratch/large/DiscoPromptClassification_PDTB2_03LRScratchPFT14may \
--prompt_lr 0.3 \
--epoch 1_000_000 \
--percentage 1 \
--project_root "/local/musaeed/DiscoPrompt" > "/local/musaeed/NPIDRC/FullTransferMethod/Results/DiscoPrompt/Scratch/PFT/t5_v1_1_large/t5V1_1_largeLog_0_3_learningRate_1M_epochs_PFTScratch.txt"

