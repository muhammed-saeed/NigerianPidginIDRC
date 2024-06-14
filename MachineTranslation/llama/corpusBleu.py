import sacrebleu
 
refs = [ # First set of references
          ['The dog bit the man.', 'It was not unexpected.', 'The man bit him first.'],
             # Second set of references
             ['The dog had bit the man.', 'No one was surprised.', 'The man had bitten the dog.'],
           ]
sys = ['The dog bit the man.', "It wasn't surprising.", 'The man had just bitten him.']

print(sacrebleu.corpus_bleu(sys, refs))
