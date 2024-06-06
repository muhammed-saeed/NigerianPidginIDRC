en = open("/local/musaeed/NPIDRC/AlignmentCenteric/giza-py/textFiles/english.txt").readlines()
pcm = open("/local/musaeed/NPIDRC/AlignmentCenteric/giza-py/textFiles/pcm.txt").readlines()
en.extend(open("/local/musaeed/NPIDRC/AlignmentCenteric/giza-py/pdtbText/en.txt").readlines())
pcm.extend(open("/local/musaeed/NPIDRC/AlignmentCenteric/giza-py/pdtbText/pcm.txt").readlines())

with open("/local/musaeed/NPIDRC/AlignmentCenteric/giza-py/allFilesTogether/english.txt", "w") as fb:
    fb.writelines(en)

with open("/local/musaeed/NPIDRC/AlignmentCenteric/giza-py/allFilesTogether/pcm.txt", "w") as fb:
    fb.writelines(pcm)
