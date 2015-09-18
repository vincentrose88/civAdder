import sys

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
#    for wordNr in range(0,len(splittedLine)):
        word=splittedLine[wordNr]
        if(word[len(word)-1]=='.' or word[len(word)-1]==','):
            cleanword = word[:-1]
            punct = word[len(word)-1]
        else:
            cleanword = word
            punct = ''

        word = cleanword
#        print(word)
 #       print(wordNr)
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



