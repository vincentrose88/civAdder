import sys

if(sys.argv[1]=='-h' or sys.argv[1]=='--help'):
    print(
        'For Civilization Battle Royal Mk.II community at '
        'reddit/r/civbattleroyale - Flair up!\n'
        'This python script takes in a plain text file as the only argument.\n'
        'It adds civilization names in brackets to leader names (from the '
        'civBR_civ_leader.tsv).\n'
        'Outputs a new text-file with a suffix: "_with_civs".\n'
        'Made by vincentrose88')
    exit(0)

input_file = str(sys.argv[1])
input_lines = open(input_file,'r').readlines()

#Reads in a file with civs mapped to leaders and add it to a dic
civ_leader_file = open('civBR_civ_leader.tsv','r')
civ_leader = {leader.strip('\n'): country
              for line in civ_leader_file
              for (country, leader) in [line.split('\t')]}

def find_best_leader_match(input_lines):
    """Return best leader according to input.

    Finds the best matched leader name for inputted list of words (containing
    at least one leadername) (useful when narrator use shortned leader names
    and more leaders share some of their name (Khan as an example)."""
    best_match = 0
    matched_key = None
    output = ''
    for leader in civ_leader.keys():
        matches = 0
        for split_name in leader.split():
            for split_input in input_lines:
                if(split_input == split_name):
                    matches+=1

        if(matches>best_match):
            matched_key = leader
            best_match = matches
        elif(matches==best_match and matches!=0):
            matched_key = None

    if(matched_key is not None):
        output= civ_leader[matched_key]

    return(output)


#Reads in all leader names in the leader_civ dic to filter narrator text
all_names = [k for keys in civ_leader for k in keys.split()]

updated_file = open(input_file + '_with_civs','w')
#Reads in a text file from narrators and searches for leadernames and adds civ in brackets
for line in input_lines:
    new_line = ''
    split_line = line.split(' ')
    start_word_number = 0
    word_number = 0
    while word_number < len(split_line):
        word=split_line[word_number]
        if(word[len(word)-1] in '.,:;?!+-='):
            cleanword = word[:-1]
            punct = word[len(word)-1]
        else:
            cleanword = word
            punct = ''

        word = cleanword
        w=0
        leader = []
        if(word in all_names and word !='I'):
            while(word in all_names):
                leader.append(word)
                w +=1
                word = split_line[word_number+w]

            civ = find_best_leader_match(leader)

            if(civ!=''):
                updated_info = ' {} ({}){} '.format(
                    ' '.join(leader), civ, punct)
                new_line = new_line + ' '.join(split_line[start_word_number:word_number]) + updated_info
                start_word_number = word_number + len(leader)
                word_number = word_number + len(leader)
            else:
                word_number += 1
        else:
            word_number += 1

    new_line = new_line + ' '.join(split_line[start_word_number:])

    updated_file.write(new_line)

