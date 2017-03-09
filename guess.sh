#IN: data/wordforms_counted_nolower.txt

cat data/wordforms_counted_nolower.txt | rev | cut -d" " -f 1 | rev > data/data_in

split -a 5 -d -l 10000 data/data_in data/part_datain_

for f in data/part_datain_* ; do echo $f ; cat $f | hfst-guess -g 0.0 -m 10000 -n 10000 /home/ginter/ParseBank/omorfi-trunk/MODEL/finn.guess.hfst | gzip > $f.guessed.gz ; done

zcat data/*.guessed.gz | gzip > data/wordforms.guessed.txt.gz
#OUT: data/wordforms.guessed.txt.gz

#Cleanup
#rm -f part_datain_* data_in
