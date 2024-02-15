#!/bin/tcsh -f


set dir=$argv[1]
echo "Cleaning git repo in path: $dir"


cd $dir
pwd

git rm -rf *
git commit -m 'Cleared'
git checkout --orphan tmp-master
set d = `date`
echo "Cleared $d" >> log.txt
git add log.txt
git commit -m 'Add to log.txt.'
git branch -D master
git branch -m master
git push -f origin master


