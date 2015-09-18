import sys

if(sys.argv[1]=='-h' or sys.argv[1]=='--help'):
    print('For Civilization Battle Royal Mk.II community at reddit/r/civbattleroyale - Flair up!\nThis python script takes in a plain text file as the only argument.\nIt adds civilization names in brackets to leader names (from the civBR_civ_leader.tsv).\nOutputs a new text-file with a suffix: "_with_civs".\nMade by vincentrose88')
    exit(0)

inputted_file = str(sys.argv[1])
inputted = open(inputted_file,'r').readlines()

#Reads in a file with civs mapped to leaders and add it to a dic
civ_leader_file = open('civBR_civ_leader.tsv','r')
civ_leader = {}
for line in civ_leader_file:
    i = line.split('\t')
    civ_leader[i[1].strip('\n')]=i[0]


def find_best_leader_match(inputted):
    "Finds the best matched leader name for inputted list of words (containing at least one leadername) (useful when narrator use shortned leader names and more leaders share some of their name (Khan as an example)"
    best_match = 0
    matched_key = 'Not found'
    output = ''
    for i in civ_leader.keys():
        j=i.split()
        matches = 0
        for n in j:
            for m in inputted:
                if(m==n):
                    matches+=1

        if(matches>best_match):
            matched_key = i
            best_match = matches
        elif(matches==best_match and matches!=0):
            matched_key = 'Not found'
            
    if(matched_key!='Not found'):
        output= civ_leader[matched_key]

    return(output)


#Reads in all leader names in the leader_civ dic to filter narrator text
allNames = []
for keys in civ_leader.keys():
    splittedKeys = keys.split()
    for k in splittedKeys:
        allNames.append(k)

updatedFile = open(inputted_file + '_with_civs','w')
#Reads in a text file from narrators and searches for leadernames and adds civ in brackets
for line in inputted:
    newLine = ''
    splittedLine = line.split(' ')
    startWordNr = 0
    wordNr = 0
    while wordNr < len(splittedLine):
        word=splittedLine[wordNr]
        if(word[len(word)-1]=='.' or word[len(word)-1]==','):
            cleanword = word[:-1]
            punct = word[len(word)-1]
        else:
            cleanword = word
            punct = ''

        word = cleanword
        w=0
        leader = []
        if(word in allNames and word !='I'):
            while(word in allNames):
                leader.append(word)
                w +=1
                word = splittedLine[wordNr+w]

            civ = find_best_leader_match(leader)

            if(civ!=''):
                updatedInfo = ' '+' '.join(leader)+' ('+civ+')' + punct + ' '
                newLine = newLine + ' '.join(splittedLine[startWordNr:wordNr]) + updatedInfo
                startWordNr = wordNr + len(leader)
                wordNr = wordNr + len(leader)
            else:
                wordNr += 1
        else:
            wordNr += 1

    newLine = newLine + ' '.join(splittedLine[startWordNr:])

    updatedFile.write(newLine)

