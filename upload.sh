datestamp=$(date +"%Y-%m-%d-%H-%M")


git add -A
git branch -M main
git commit -m $datestamp
git remote add origin  https://github.com/Dennis-Spera/jaguar.git
git push -u origin master
git push https://github.com/Dennis-Spera/jaguar.git