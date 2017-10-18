import sys
ID,FORM,LEMMA,UPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

def read_conllu(f):
    for line in f:
        line=line.strip()
        if not line or line.startswith("#"):
            continue

        token=line.split("\t")
        yield token[FORM],token[LEMMA],token[UPOS],token[FEAT]

def read_tsv(f):
    for line in f:
        yield line.split("\t")


def print_token(word,lemma,pos,feat,args,out_in,out_out=None):


    if args.no_tags:
        wf=" ".join(word)
    else:
        wf=" ".join(list(word)+["t="+pos]+["t="+t for t in feat.split("|")])
    lemma=" ".join(list(lemma))
    print(wf,file=out_in)
    if out_out is not None:
        print(lemma,file=out_out)
  

def main(args):
    if len(args.input_file)>0:
        f=open(args.input_file,"rt",encoding="utf-8")
    else:
        f=sys.stdin
    if args.format=="conllu":
        data_iter=read_conllu(f)
    else:
        data_iter=read_tsv(f)
        
    # output files
    out_in=open(args.output_files+".in","wt",encoding="utf-8")
    if args.just_input:
        out_out=None
    else:
        out_out=open(args.output_files+".out","wt",encoding="utf-8")
    
    # iter data    
    for word,lemma,pos,feat in data_iter:
        
        print_token(word,lemma,pos,feat,args,out_in,out_out)

    out_in.close()
    if out_out is not None:
        out_out.close()      
    
if __name__=="__main__":

    import argparse

    parser = argparse.ArgumentParser(description='')
    g=parser.add_argument_group("Arguments")
    g.add_argument('-i', '--input_file', type=str, default='', help='Input file name')
    g.add_argument('-o', '--output_files', type=str, required=True, help='Output file name(s), creates output_file.in and output_file.out')
    g.add_argument('--format', type=str, default='conllu', help='File format, default=conllu, other options: csv (tab separated wordform, lemma, pos, features)')
    g.add_argument('--no_tags', action='store_true', default=False, help='Do not output POS or morphological tags')
    g.add_argument('--just_input', action='store_true', default=False, help='create only input file, not gold output)')  
    
    args = parser.parse_args()
    
    main(args)
