# github-query-script

Following are the steps to execute both scripts:
1.	In case of windows, open a command prompt or windows power shell.
2.	With python setup already completed, first make sure that github3 API is already installed, if not then run the following command:
pip install --pre github3.py 
https://github.com/sigmavirus24/github3.py
3.	Delete any old “repositories.txt” or “code.csv” files in the directory where the scripts are present so that the following script can create a new file with the latest results.
4.	Then update both get_matching_repositories.py and get_matching_code_files.py scripts with valid GitHub username and password.
5.	Now go to the directory via command prompt or power shell where the scripts are present.
6.	To execute the first python script, run the following command:
    python get_matching_repositories.py
This will extract Java repositories and export their information into “repositories.txt” file as explained in the previous section.
7.	Now in order to execute the second script, run the following command:
python get_matching_code_files.py --username <githubusername> --repoFile repositories.txt --outputFile code.csv
This will give the final results in a “code.csv” file which would have the list of repositories along with the file names which are using javax.crypto library as explained in the previous section.
