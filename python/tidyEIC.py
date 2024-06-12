#tidyEIC.py

import os 
import argparse 


def tidyEIC(csv_in):

    #initialize empty objects
    hash_index = []
    hash_lines = {}

    with open(csv_in, 'r') as infile:
        #read initial information
        for idx, line in enumerate(infile):
            if line.startswith('#'):
                hash_index.append(idx)
                hash_lines[idx] = line.strip()

    #assign row indices for sample names and those with column headers
    experiment_indices = hash_index[::2]
    column_indices = hash_index[1::2]
    header_dict = {key: hash_lines[key] for key in experiment_indices}

    #initialize new list of sample names
    sample_names = []

    #loop through header_dict and extract sample names from .d file name 
    for exp in experiment_indices:
        string = header_dict[exp]
        
        #sample name is in between the last two spaces in this entry
        #pull everything in between and get rid of '.d'

        last_space = string.rfind(' ')
        pen_space = string.rfind(' ', 0, last_space)

        sample_name = string[pen_space + 1: last_space - 2]
        
        #add sample name to list of names
        sample_names.append(sample_name)

    #open EIC csv file again to add new column of values containing sample name
    with open(csv_in, 'r') as infile:
        lines = infile.readlines()
        
        #initialize index to keep track of which sample name gets written
        sample_number = 0 #first sample

        while sample_number < len(sample_names) - 1:

            #now loop through each line of the file
            for row in range(column_indices[sample_number] + 1,
                             experiment_indices[sample_number + 1]):
                lines[row] = lines[row].rstrip('\n') + ',' + sample_names[sample_number] + '\n'

            sample_number += 1

        #this will do all but the last set of data so we do that separately
        for row in range(column_indices[sample_number] + 1,len(lines)):
            lines[row] = lines[row].rstrip('\n') + ',' + sample_names[sample_number] + '\n'

        #now determine which lines should remain after removing the hash lines
        data_lines = [line for i, line in enumerate(lines) if i not in
                      hash_index]

    # create a final csv output with data and a single header line == tidy
    new_header = 'point,time,count,sample\n'

    with open(os.path.splitext(csv_in)[0] + '_tidy.csv', 'w') as outfile:

        #write new header as first row
        outfile.write(new_header)

        #write data starting after the header
        outfile.writelines(data_lines)


# function that is called when run from command line
def main():

    #argument parser
    parser = argparse.ArgumentParser(description='Convert MassHunter csv format EIC to tidy format csv data')

    parser.add_argument('file', type=str, help='The path to the MassHunter csv input file')

    #parse arguments 
    args = parser.parse_args() 

    #call functions that generate tidy data
    tidyEIC(args.file)

if __name__ == "__main__":
    main()
