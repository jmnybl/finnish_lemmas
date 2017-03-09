import sys

def build_dict():
    d={}
    for line in open("wordforms_counted_nolower.txt","rt"):
        c,word=line.strip().split(" ")
        d[word]=c
    return d

d=build_dict()

for line in sys.stdin:
    line=line.strip()
    cols=line.split("\t")
    if len(cols)==1:
        print(line)
    else:
        word=cols[0]
        w_count=0
        if word in d:
            w_count=d[word]
        lemma=cols[1].split("[",1)[0]
        if lemma in d:
            print(line,w_count,d[lemma],sep="\t")
        #else: # candidate lemma has zero count in parsebank
        #    print(line,w_count,0,sep="\t")
