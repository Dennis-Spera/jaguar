datestamp=$(date +"%Y-%m-%d-%H-%M")

#kadmin@jupiter:~/Dropbox/projects/jaquar$ bash upload.sh
#[detached HEAD c23aa65] 2025-03-07-09-54
# 1 file changed, 1 insertion(+)
#To https://github.com/Dennis-Spera/jaguar.git
# ! [rejected]        HEAD -> main (fetch first)
#error: failed to push some refs to 'https://github.com/Dennis-Spera/jaguar.git'
#hint: Updates were rejected because the remote contains work that you do not
#hint: have locally. This is usually caused by another repository pushing to
#hint: the same ref. If you want to integrate the remote changes, use
#hint: 'git pull' before pushing again.
#hint: See the 'Note about fast-forwards' in 'git push --help' for details.

# -> solution below
#kadmin@jupiter:~/Dropbox/projects/jaquar$ git pull https://github.com/Dennis-Spera/jaguar.git HEAD:main


git add -A
#git branch -M main
git commit -m $datestamp
#git remote add origin  https://github.com/Dennis-Spera/jaguar.git
#git push -u or
git push https://github.com/Dennis-Spera/jaguar.git HEAD:main