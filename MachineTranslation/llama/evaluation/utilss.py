def ListWriter(fname, list):
    with open(fname, "w") as fb:
        for item in list:
            fb.write("%s\n"%item)
        print("Done")
