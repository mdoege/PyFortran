# Fortran interpreter

import sys, array
from math import *
from functools import reduce
from operator import mul

fn = sys.argv[1]
if len(sys.argv) > 2:
    infn = sys.argv[2]
    infile = open(infn)

srco = open(fn).readlines()
srco = [q.upper() for q in srco]
src = []
for x in srco:
    l = x[:72].rstrip()
    # remove indentation:
    if len(l) > 6:
        l = l[:6] + l[6:].strip()
    if len(l) > 5 and l[5] != " " and l[5] != "0" and l[0] != "C":
        # concatenate continuation lines
        src[-1] += l[6:].strip()
    else:
        src.append(l)

#for l in src: print(l)
cur = 0

lab = {}    # labels
var = {}    # variables
loops = {}  # loops
arr = {}    # arrays

# built-in functions
funcs = ("SINF", "COSF", "INTF", "SQRTF", "XMODF", "EXPF", "LOGF", "ATANF", "FLOATF")

def SINF(x):
    return sin(x)

def COSF(x):
    return cos(x)

def INTF(x):
    return int(x)

def SQRTF(x):
    return sqrt(x)

def EXPF(x):
    return exp(x)

def LOGF(x):
    return log(x)

def ATANF(x):
    return atan(x)

def FLOATF(x):
    return float(x)

def XMODF(a, b):
    return a % b

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
    i = 0
    while i < len(l):
        x = l[i]
        if x.isalpha() and len(v) == 0:
            v += x
        elif x.isalnum() and len(v) > 0:
            v += x
        else:
            if len(v):
                if v in funcs:  # built-in function
                    o += v
                elif v in arr:  # array
                    aind = [int(eval(repvar(q))) for q in parse_ind(l[i:])]
                    a, adims = arr[v]
                    aind1 = get_ind(aind, adims)
                    o += str(arr[v][0][aind1])
                    i = l.find(")", i) + 1
                    v = ""
                    continue
                else:           # scalar variable
                    o += str(var[v])
                v = ""
            o += x
        i += 1
    return o[:-1]

def parse_ind(x):
    # Parse array index from text
    par = x.find(")")
    out = x[1:par].split(",")
    #print(out)
    return out

def get_ind(index, dims):
    # Get 1-dimensional index from multi-dimensional index
    q = 0
    for i in range(len(dims)):
        if i > 0:
            q += (index[i] - 1) * dims[i-1]
        else:
            q += (index[i] - 1)
    return q

def makeform(t):
    # Create Python format string
    out = ""
    for x in t:
        if x.isdigit() or x == ".":
            out += x
        else:
            break
    return out

def reformat(t):
    # Apply FORMAT to output
    f = src[lab[str(t[0])]]
    par = f.find("(")
    f = f[par:]

    num = ""
    i = 0
    out = ""
    vi = 1
    #print(t,f)
    while i < len(f):
        x = f[i]
        if x == ",":
            num = ""
        if x.isdigit():
            num += x
        if x == "H":
            out += f[i+1:i+1+int(num)]
            i += int(num) + 1
            num = ""
            continue
        if x == "F":
            digtext = f[i+1:]
            digtext = "%" + makeform(digtext) + "f"
            out += digtext % t[vi]
            vi += 1
            i += 1
            continue
        if x == "E":
            digtext = f[i+1:]
            digtext = "%" + makeform(digtext) + "e"
            out += digtext % t[vi]
            vi += 1
            i += 1
            continue
        if x == "I":
            digtext = f[i+1:]
            digtext = "%" + makeform(digtext) + "i"
            out += digtext % t[vi]
            vi += 1
            i += 1
            continue
        i += 1
    return out

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
    if "=" in line and not beg("DO") and not beg("FORMAT"):
        left, right = line.split("=")
        right = repvar(right)
        if "(" in left: # array
            par = left.find("(")
            aname = left[:par]
            aind = [int(eval(repvar(q))) for q in left[par+1:-1].split(",")]
            #print(aind)
            a, adims = arr[aname]
            aind1 = get_ind(aind, adims)
            arr[aname][0][aind1] = eval(right)
            #print(arr[aname])
        else:
            var[left] = eval(right)
        #print(var[left])

    if beg("DIMENSION"):
        v = line[9:].split(")")
        for x in v:
            if len(x) == 0:
                continue
            par = x.find("(")
            aname = x[:par].replace(",", "")
            adims = [int(q) for q in x[par+1:].split(",")]
            #print(aname, adims)
            an = array.array("d", [0] * reduce(mul, adims))
            arr[aname] = an, adims

    if beg("PRINT"):
        out = eval(repvar(line[5:]) + ",")
        if line[5].isdigit():
            out = reformat(out)
            print(out)
        else:
            for x in out:
                print(x, "  ", end = "")
            print()

    if beg("READ"):
        v = line[4:].split(",")
        for x in v:
            if x[0].isalpha():
                var[x] = float(infile.readline())

    if beg("PUNCH"):
        v = line[5:].split(",")
        for x in v:
            if len(x) > 0:
                print("%12u" % var[x], end = "")
        print()

    if beg("ACCEPT"):
        v = line[6:].split(",")
        for x in v:
            if x[0].isalpha():
                var[x] = input(x + "=? ")

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
        targ = line[4:].strip()
        if targ[0] == "(":  # computed GO TO
            par = targ.find(")")
            dest = targ[1:par].split(",")
            v = eval(repvar(targ[targ.rfind(",") + 1:]))
            cur = lab[dest[v - 1]]
            continue
        else:               # normal GO TO
            cur = lab[targ]
            continue

    if beg("IF (") or beg("IF("):
        par = line.rfind(")")
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


