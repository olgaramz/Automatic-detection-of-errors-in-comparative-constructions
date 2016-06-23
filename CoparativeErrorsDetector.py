import os
import re

allSentences = []
newList = []
global intens
intens = []

def searchErrorsType1(lst):
    log = []
    for ind, word in enumerate(lst):
        m = re.search('[Бб]олее', word)
        if m != None:
            try:
                nxt = lst[ind + 1]
                n = re.search('A(DV)?=.*?(срав|прев)', nxt)
                if n != None:
                    try:
                        prv = lst[ind - 1]
                        k = re.search('[Тт]ем{то=SPRO', prv)
                        if k == None:
                            error = '[ошибка первого типа]'
                            log.append(error)
                    except IndexError:
                        continue
            except IndexError:
                pass
        else:
            l = re.search('[Мм]енее', word)
            if l != None:
                try:
                    nxt = lst[ind + 1]
                    n = re.search('A(DV)?=.*?(срав|прев)', nxt)
                    if n != None:
                        try:
                            prv = lst[ind - 1]
                            prv2 = lst[ind-2]
                            q = re.search('[Бб]олее', prv)
                            if q == None:
                                k = re.search('{не=PART=', prv)
                                if k != None:
                                    p = re.search('[Тт]ем{то=SPRO', prv2)
                                    if p == None:
                                        error = '[ошибка первого типа]'
                                        log.append(error)
                                else:
                                    error = '[ошибка первого типа]'
                                    log.append(error)
                        except IndexError:
                            continue
                except IndexError:
                    pass
    return log  
    
    
def searchErrorsType2(lst):
    log = []
    for ind, word in enumerate(lst):
        m = re.search('нежели=CONJ', word)
        if m != None:
            try:
                nxt = lst[ind + 1]
                n = re.search('чем=CONJ', nxt)
                if n != None:
                    error = '[ошибка второго типа]'
                    log.append(error)
                else:
                    try:
                        prv = lst[ind - 1]
                        k = re.search('чем=CONJ', prv)
                        if k != None:
                            error = '[ошибка второго типа]'
                            log.append(error)
                    except IndexError:
                        continue
            except IndexError:
                pass
    return log

def searchErrorsType3(lst):
    log = []
    for ind, word in enumerate(lst):
        for j in intens:
            advInd = word.find(j)
            if advInd != -1:
                try:
                    nxt = lst[ind + 1]
                    nxt2 = lst[ind + 2]
                    m = re.search('=A(DV)?=.+?,(полн|кр)', nxt)
                    if m != None:
                        n = re.search('чем{чем=CONJ', nxt2) #new
                        if n == None:
                            t = re.search('нежели=CONJ', nxt2) #new
                            if t != None:
                                error = '[ошибка третьего типа]'
                                log.append(error)
                        else:
                            error = '[ошибка третьего типа]'
                            log.append(error)
                except IndexError:
                    pass
    return log
    

filename = 'testsetCompar.txt'

with open('advlist.txt', 'r', encoding = 'utf-8') as advlist:
    for line in advlist:
        line = line.replace('\n', '')
        intens.append(line)

command = 'C:\\mystem.exe -cid ' + filename + ' C:\\Users\\Asus\\Desktop\\mystemout.txt'
os.system(command)

with open('C:\\Users\\Asus\\Desktop\\mystemout.txt', 'r', encoding = 'utf-8') as text:
    for line in text:
        m = re.split('(?<=})[\.!\?…"](?=\s+[А-ЯЁ[(])', line)
        for i in m:
            allSentences.append(i)
    
for j in allSentences:
    words = j.split(' ')
    result = searchErrorsType1(words)
    result2 = searchErrorsType2(words)
    result3 = searchErrorsType3(words)
    sent = ''.join(j)
    errors = ';'.join(result)
    errors2 = ';'.join(result2)
    errors3 = ';'.join(result3)
    p = sent + '\t' + errors + '\t' + errors2 + '\t' + errors3 + '\n'
    newList.append(p)

s = ''.join(newList)

with open('searchresult.txt', 'w', encoding = 'utf-8') as f:
    f.write(s)
