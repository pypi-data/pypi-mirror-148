

def namesplit(inputName):
    fname = list(inputName)
    songname = ''
    hyphc = 0
    for i in range(len(fname)):
        if fname[i] == '(' or fname[i] == '{' or fname[i] == '|' or fname[i] == '[':
            break
        if fname[i] == '-':
            hyphc += 1
        if fname[i] == '-' and hyphc == 2:
            break
        songname += str(fname[i])
    
    return songname