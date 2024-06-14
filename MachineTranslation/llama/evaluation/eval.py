import sacrebleu
from utils import twoListWriters
# Initialize empty lists for instructions, pcm_inputs, and en_outputs
instructions = []
pcm_inputs = []
en_outputs = []

# Read the dataset file line by line
with open('/PATH_TO/general-pidgin-modeling/llama/evaluation/test_english_preds.txt', 'r') as file:
    lines = file.readlines()

# Process each line in the dataset
def procesFiles(lines):
    inputs = []
    outputs = []
    for line in lines:
        line = line.strip()
        
        # Check if the line starts with 'Instruction:'
        if line.startswith('instruction:'):
            instruction = line[len('instruction:'):].strip()
            instructions.append(instruction)
        
        # Check if the line starts with 'Input:'
        elif line.startswith(', Input:'):
            input_text = line[len(', Input:'):].strip()
            inputs.append(input_text)
            
        # Check if the line starts with 'Output:'
        elif line.startswith(', Output:'):
            output_text = line[len(', Output:'):].strip()
            outputs.append(output_text)
    return inputs, outputs

pcm_inputs, en_predictions = procesFiles(lines)

lines = []
with open('/PATH_TO/general-pidgin-modeling/llama/evaluation/test_pcm_preds.txt', 'r') as file:
    lines = file.readlines()

en_inputs = []
pcm_predictions = []
 
en_inputs, pcm_predictions = procesFiles(lines)

# Print the extracted instructions, pcm_inputs, and en_outputs
print(f"{en_predictions[50]}")
print(f"{len(en_predictions)}")
print(f"{pcm_inputs[50]}")
print(f"{len(pcm_inputs)}")
##
##
print(f"{en_inputs[50]}")
print(f"{len(en_inputs)}")
print(f"{pcm_predictions[50]}")
print(f"{len(pcm_predictions)}")


from sacrebleu import corpus_bleu
bleu = corpus_bleu(pcm_predictions, pcm_inputs)
print(f"english to pcm blue scoer is {bleu}")
bleu = corpus_bleu(en_predictions, en_inputs)
print(f"pcm to english blue scoer is {bleu}")

twoListWriters("llama/evaluation/lists/hypoTrue/pcmFile.txt",pcm_inputs, pcm_predictions)
twoListWriters("llama/evaluation/lists/hypoTrue/enFile.txt",en_inputs, en_predictions)