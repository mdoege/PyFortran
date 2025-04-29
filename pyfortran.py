# Fortran interpreter

import sys
from math import *

fn = sys.argv[1]

srco = open(fn).readlines()
srco = [q.upper() for q in srco]
src = []
for x in srco:
    l = x[:72].rstrip()
    # remove indentation:
    if len(l) > 6:
        l = l[:6] + l[6:].strip()
    if len(l) > 5 and l[5] != " " and l[5] != "0":
        src[-1] += l[6:].strip()
    else:
        src.append(l)

#for l in src: print(l)
cur = 0

lab = {}    # labels
var = {}    # variables
loops = {}  # loops

# built-in functions
funcs = ("COSF", "INTF", "SQRTF")

def COSF(x):
    return cos(x)

def INTF(x):
    return int(x)

def SQRTF(x):
    return sqrt(x)

def beg(cmd):
    # check for Fortran keyword
    if src[cur][6:6+len(cmd)] == cmd:
        return True
    else:
        return False

def repvar(l):
    # replace variable names with contents
    l += "?"
    o = ""
    v = ""
    for x in l:
        if x.isalpha() and len(v) == 0:
            v += x
        elif x.isalnum() and len(v) > 0:
            v += x
        else:
            if len(v):
                if v in funcs:
                    o += v
                else:
                    o += str(var[v])
                v = ""
            o += x
    return o[:-1]

# check for all labels
for l in range(len(src)):
    curlab = src[l][:5].strip()
    if curlab != "":
        lab[curlab] = l

while True:
    if len(src[cur]) > 0 and src[cur][0] == "C":  # skip comment lines
        #print(src[cur].strip())
        cur += 1
        continue

    #print(cur, src[cur])

    # check for current label
    curlab = src[cur][:5].strip()

    if beg("STOP") or beg("END"):
        break

    line = src[cur][6:].replace(" ", "").strip()

    # assignment
    if "=" in line and not beg("DO"):
        left, right = line.split("=")
        right = repvar(right)
        var[left] = eval(right)
        #print(var[left])

    if beg("PRINT"):
        print(repvar(line[5:]))

    if beg("PUNCH"):
        v = line[5:].split(",")
        for x in v:
            if len(x) > 0:
                print("%12u" % var[x], end = "")
        print()

    if beg("DO"):
        left, right = line.split("=")
        right = repvar(right)
        lim = eval(right)
        va = "".join([q for q in left if q.isalpha()])[2:]
        la = "".join([q for q in left if not q.isalpha()])
        var[va] = lim[0]
        if len(lim) > 2:
            inc = lim[2]
        else:
            inc = 1
        newloop = loops.get(la, [])
        newloop.append((va, lim[1], inc, cur))
        loops[la] = newloop
        #print(va, la, inc)

    if beg("GO TO") or beg("GOTO"):
        cur = lab[line[4:].strip()]
        continue

    if beg("IF"):
        par = line.find(")")
        test = line[3:par]
        targ = line[par+1:].split(",")
        v = eval(repvar(test))
        if v < 0:
            cur = lab[targ[0].strip()]
        elif v > 0:
            cur = lab[targ[2].strip()]
        else:
            cur = lab[targ[1].strip()]
        continue

    if beg("PAUSE"):
        print("*** program paused; press Return to continue")
        input()

    # check if on final line of a loop
    if curlab in loops.keys() and len(loops[curlab]) > 0:
        #print(loops[curlab])
        while len(loops[curlab]) > 0:
            va, lim, inc, lnum = loops[curlab][-1]
            var[va] += inc
            if var[va] + inc > lim: # final iteration?
                loops[curlab].pop()
            if var[va] <= lim:
                cur = lnum + 1
                break
    else:   # advance to next line
        cur += 1
        if cur >= len(src): # check if end of file
            break


