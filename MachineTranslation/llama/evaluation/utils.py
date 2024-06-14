def twoListWriters(file_path, list1, list2):
    with open(file_path, 'w') as file:
        # Iterate over the items in the lists
        for item1, item2 in zip(list1, list2):
            # Write the items to the file
            file.write(f'true sentence: {item1}\nhypothesis: {item2}\n')
            file.write("- - - - - - - - - - - - - - -  -  - - - - - - - \n")