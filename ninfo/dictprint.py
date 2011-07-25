#!/usr/bin/env python

def pdicthtml(d, order=None):
	res="<tr>"
	if order is None:
		for x in d:
			res += "<td>%s</td>" % (d[x])
	else :
		for x in order:
			res += "<td>%s</td>" % (d[x])
	return res + "</tr>"


def pdict(d, order=None):
	data=[]
	if order is None:
		for x in d:
			data.append("%s: %s" % (x, d[x]))
	else :
		for x in order:
			data.append("%s: %s" % (x, d[x]))
	print ", ".join(data)


def justify(d, order=None):
    """Print out a nice verticle table"""

    if order:
        it = order
    else:
        it = d
    
    size = 1+ max([len(x) for x in it])
    #build a string like '%-11s: %s' using $ temporarily for simplicity
    temp  = "$-%ds: $s" % size
    format = temp.replace("$", "%")

    for k in it:
        print format % (k, d[k])

def dictarrayprint(ar, order=None, header=True):
    #allow for an empty array
    #if the array is empty and no order is paseed, return ""
    #otherwise generate just the header
    if not ar:
        if not order:
            return ""
        first = dict([(x,x) for x in order])
    else :
        first = ar[0]
    if header: #insert a new row of just the keys, the next loop will do the rest
        new = dict([(x,str(x).capitalize()) for x in first.keys()]) 
        new = [new]
    else :
        new = []
    #figure out what the longest column in each row is
    maxes = dict([(a,len(str(b))) for a,b in first.items()])
    for x in new + ar:
        for k, v in x.items():
            size = len(str(v))
            if size > maxes[k]:
                maxes[k] = size
    
    maxesfmt = dict([(x, "%%-%ds" % (y+1)) for x,y in  maxes.items()])
    if order:
        it = order
    else :
        it = first #will iterate over the keys however
    
    table = []

    for x in new + ar:
        row = []
        for c in it:
            row.append( maxesfmt[c] % x[c] )
        line = " ".join(row).strip()
        table.append(line)

    return "\n".join(table)

if __name__ == "__main__":
	a=[]
	d={'name': "justin", 'age': 21, 'foo': 12345}
	pdict(d)
	pdict(d, ("foo","name","age"))
