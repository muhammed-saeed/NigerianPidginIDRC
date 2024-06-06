
CUDA_VISIBLE_DEVICES=3 python /local/musaeed/DiscoPrompt/DiscoPromptPidginContinueFromCheckpoint.py \
--template_id 0 --max_steps 30000 \
--csv_file_path "/local/musaeed/NPIDRC/BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAEAwesomeAlignFinetunedPostProcessed.csv" \
--batch_size 8 --eval_every_steps 250 \
--shouldResumeTrainingFromCheckpoint True \
--resume_from_checkpoint "/local/musaeed/DiscoPrompt/ckpts/englishBaseT5_v_1_large/DiscoPromptClassification_PDTB2.ckpt" \
--dataset ji --model_name_or_path google/t5-v1_1-large \
--result_file /local/musaeed/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/CaFT/PFT/t5_v1_1_large/03LearningRateDiscoPromptClassification_PDTB2CaFT8batchsize.txt \
--ckpt_file AlignOnly/PFT/CaFT/large/DiscoPromptClassification_PDTB2_03LRAkramAlignCaFTPFT8batchSize \
--prompt_lr 0.3 \
--epoch 1_000_000 \
--percentage 1 \
--project_root "/local/musaeed/DiscoPrompt" > "/local/musaeed/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/CaFT/PFT/t5_v1_1_large/t5V1_1_largeLog_0_3_learningRate_1M_epochs_PFTCaFT8batchsize.txt"

