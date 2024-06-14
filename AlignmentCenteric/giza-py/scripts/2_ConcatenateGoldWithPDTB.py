en = open("/PATH_TO/NPIDRC/AlignmentCenteric/giza-py/textFiles/english.txt").readlines()
pcm = open("/PATH_TO/NPIDRC/AlignmentCenteric/giza-py/textFiles/pcm.txt").readlines()
en.extend(open("/PATH_TO/NPIDRC/AlignmentCenteric/giza-py/pdtbText/en.txt").readlines())
pcm.extend(open("/PATH_TO/NPIDRC/AlignmentCenteric/giza-py/pdtbText/pcm.txt").readlines())
with open("/PATH_TO/NPIDRC/AlignmentCenteric/giza-py/allFilesTogether/english.txt", "w") as fb:
    fb.writelines(en)
with open("/PATH_TO/NPIDRC/AlignmentCenteric/giza-py/allFilesTogether/pcm.txt", "w") as fb:
    fb.writelines(pcm)
