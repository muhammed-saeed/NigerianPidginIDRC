
CUDA_VISIBLE_DEVICES=0 python /PATH_TO/DiscoPrompt/DiscoPromptPidginContinueFromCheckpoint.py \
--template_id 0 --max_steps 30000 \
--csv_file_path "/PATH_TO/NPIDRC/BMGF-RoBERTa/data/csvBMGFColumns/pdtbPDTBRemovedTNFAndAEAwesomeAlignFinetunedPostProcessed.csv" \
--batch_size 4 --eval_every_steps 250 \
--shouldResumeTrainingFromCheckpoint True \
--resume_from_checkpoint "/PATH_TO/DiscoPrompt/ckpts/englishBaseT5_v_1_large/DiscoPromptClassification_PDTB2.ckpt" \
--dataset ji --model_name_or_path google/t5-v1_1-large \
--result_file /PATH_TO/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/CaFT/PFT/t5_v1_1_large/03LearningRateDiscoPromptClassification_PDTB2CaFTDoubleCheck.txt \
--ckpt_file AlignOnly/PFT/CaFT/large/DiscoPromptClassification_PDTB2_03LRAkramAlignCaFTPFTDoubleCheck \
--prompt_lr 0.3 \
--epoch 1_000_000 \
--percentage 1 \
--project_root "/PATH_TO/DiscoPrompt" > "/PATH_TO/NPIDRC/FullTransferMethod/Results/DiscoPrompt/AlignOnly/CaFT/PFT/t5_v1_1_large/t5V1_1_largeLog_0_3_learningRate_1M_epochs_PFTCaFTDoubleCheck.txt"

