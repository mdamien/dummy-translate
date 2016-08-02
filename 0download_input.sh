# download the necessary dataset
wget "http://downloads.tatoeba.org/exports/sentences.tar.bz2";
bzip2 -d sentences.tar.bz2;
tar -xvf sentences.tar;
mv sentences.csv input/;
wget "http://downloads.tatoeba.org/exports/links.tar.bz2";
bzip2 -d links.tar.bz2;
tar -xvf links.tar;
mv links.csv input/;
