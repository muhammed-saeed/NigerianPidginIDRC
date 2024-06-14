from transformers import MT5Tokenizer, GPT2LMHeadModel

# Specify the directory where you want to save the model and tokenizer
save_directory = "/PATH_TO/PLM4MT/checkpoints/thump/mgpt"

# Download and save the tokenizer
tokenizer = MT5Tokenizer.from_pretrained("THUMT/mGPT")
tokenizer.save_pretrained(save_directory)

# Download and save the model
model = GPT2LMHeadModel.from_pretrained("THUMT/mGPT")
model.save_pretrained(save_directory)
