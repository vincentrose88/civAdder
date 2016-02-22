import sys

def get_civ_leader(civ_leader_file):
    """Reads in a file with civs mapped to leaders and add it to a dict.

    """
    return {leader.strip('\n'): country
            for line in civ_leader_file
            for (country, leader) in [line.split('\t')]}

def get_all_names(civ_leader):
    """Reads in all leader names in the leader_civ dict to filter narrator text.

    """
    return[k for keys in civ_leader for k in keys.split()]

def find_best_leader_match(input_lines):
    """Return best leader according to input.

    Finds the best matched leader name for inputted list of words (containing
    at least one leadername) (useful when narrator use shortned leader names
    and more leaders share some of their name (Khan as an example)."""
    best_match = 0
    matched_key = None
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
        return civ_leader[matched_key]

def insert_civ_names(input_lines, all_names):
    """Inserts civ names in parenthesis.

    Reads in a text file from narrators and searches for leader names and adds
    civ in brackets"""
    out = []
    for line in input_lines:
        new_line = []
        split_line = line.split(' ')
        start_word_num = 0
        word_num = 0
        while word_num < len(split_line):
            word=split_line[word_num]
            if(word[-1] in '.,:;?!+-='):
                punct = word[-1]
                word = word[:-1]
            else:
                punct = ''
            w = 0
            leader = []
            if(word in all_names and word != 'I'):
                while(word in all_names):
                    leader.append(word)
                    w += 1
                    word = split_line[word_num + w]
                civ = find_best_leader_match(leader)
                if civ is not False:
                    new_line.extend(
                        (' '.join(split_line[start_word_num:word_num]),
                         ' {} ({}){} '.format(' '.join(leader), civ, punct)))
                    start_word_num = word_num + len(leader)
                    word_num = word_num + len(leader)
                else:
                    word_num += 1
            else:
                word_num += 1
        new_line.append(' '.join(split_line[start_word_num:]))
        out.append(''.join(new_line))
    return(''.join(out))

def print_help():
    print (
    'For Civilization Battle Royal Mk.II community at '
    'reddit/r/civbattleroyale - Flair up!\n'
    'This python script takes in a plain text file as the only argument.\n'
    'It adds civilization names in brackets to leader names (from the '
    'civBR_civ_leader.tsv).\n'
    'Outputs a new text-file with a suffix: "_with_civs".\n'
    'Made by vincentrose88')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_help()
        exit(0)
    elif(sys.argv[1] in ('-h', '--help', None)):
        print_help()
        exit(0)
    elif(sys.argv[1]=='-t' or sys.argv[1]=='--test'):
        input_file = 'data/test_data.txt'
    else:
        input_file = str(sys.argv[1])

    input_lines = open(input_file,'r').readlines()

    civ_leader_file = open('civBR_civ_leader.tsv','r')
    civ_leader = get_civ_leader(civ_leader_file)

    all_names = get_all_names(civ_leader)

    output = insert_civ_names(input_lines, all_names)

    updated_file = open(input_file + '_with_civs', 'w')
    updated_file.write(output)
