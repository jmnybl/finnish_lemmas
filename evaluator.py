# python 3
# Use UD_Finnish v2 as gold standard data to evaluate against

import sys
import conllutil3 as cu

def read_gold_from_text(fname,remove_hash=True,save=False):
    # can also be sys.stdin
    word_lemma_pairs={} # nested dictionary, first key=form, value=dictionary, where key=(form,lemma), values=count
    for line in open(fname):
        line=line.strip()
        if not line or line.startswith("#"):
            continue
        cols=line.split("\t")
        if remove_hash:
            if "#" not in cols[cu.FORM]:
                cols[cu.LEMMA]=cols[cu.LEMMA].replace("#","")
        if cols[cu.FORM] not in word_lemma_pairs:
            word_lemma_pairs[cols[cu.FORM]]={}
        if (cols[cu.FORM],cols[cu.LEMMA]) not in word_lemma_pairs[cols[cu.FORM]]:
            word_lemma_pairs[cols[cu.FORM]][(cols[cu.FORM],cols[cu.LEMMA])]=0
        word_lemma_pairs[cols[cu.FORM]][(cols[cu.FORM],cols[cu.LEMMA])]+=1
    if save:
        pass # TODO

    return word_lemma_pairs

def read_gold_from_pickle(fname):
    pass
  
def read_predictions(fname):
    # read word--lemma distribution from predictions file
    word_lemma_pairs={}
    for line in open(fname):
        line=line.strip()
        if not line:
            continue
        cols=line.split("\t") # form, lemma, count, distr
#        print(cols)
        if cols[0] not in word_lemma_pairs:
            word_lemma_pairs[cols[0]]={}
        word_lemma_pairs[cols[0]][(cols[0],cols[1])]=float(cols[3])

    return word_lemma_pairs


def build_vectors(gold,preds):
    l2idx={}
    gold_vector=[]
    predicted_vector=[]
    word_count=sum([c for (w,l),c in gold.items()])
    for (form,lemma),c in gold.items():
        if lemma not in l2idx:
            l2idx[lemma]=len(l2idx)
            gold_vector.append(0.0)
            predicted_vector.append(0.0)
        gold_vector[l2idx[lemma]]=float(c)/word_count
    for (form,lemma),w in preds.items():
        if lemma not in l2idx:
            l2idx[lemma]=len(l2idx)
            gold_vector.append(0.0)
            predicted_vector.append(0.0)
        predicted_vector[l2idx[lemma]]=w
    return gold_vector,predicted_vector

def squared_error(gold,pred):
    return sum((i-j)**2 for i,j in zip(gold,pred))


def baseline_mostconnections(gold,predictions):
    # for each word, pick lemma which has most incoming connections
    total_error=0.0
    oov=0
    words=0
    for word in predictions:
        if word not in gold:
            oov+=1
            continue
        g,p=build_vectors(gold[word],predictions[word])
        p=[1.0 if i==p.index(max(p)) else 0.0 for i,v in enumerate(p)]
        total_error+=squared_error(g,p)
        words+=1
    return total_error/words,words,oov

def evaluate_distribution(gold,predictions):
    total_error=0.0
    oov=0
    words=0
    for word in predictions:
        if word not in gold:
            oov+=1
            continue
        g,p=build_vectors(gold[word],predictions[word])
        total_error+=squared_error(g,p)
        words+=1
    return total_error/words,words,oov # mean of squered errors of words

    

gold=read_gold_from_text("/home/jmnybl/git_checkout/UD_Finnish/fi-ud-train.conllu")
predicted=read_predictions("/home/mjluot/lemma_baseline/all_words")

e,words,oov=baseline_mostconnections(gold,predicted)
print("Baseline, most incoming connections:",e)
print("Evaluated on {} words ({} words not in gold vocabulary)".format(words,oov))
print("")
e,words,oov=evaluate_distribution(gold,predicted)
print("Baseline:",e)
print("Evaluated on {} words ({} words not in gold vocabulary)".format(words,oov))
print("")
    
