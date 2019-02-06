# github-query-script

The github-query-script consists of two independent scripts. The first script, *get_matching_repositories.py*, collects all repositories which matches to the filter criteria. Based upon these results, the second script, *get_matching_code_files.py*, generates a CSV-file with all of the in step one collected projects which use the library *javax.crypto*. 

## Executing 

Prerequirements:
- Python needs to be installed.
- Install the *github4* API for Python ``` pip install --pre github3.py https://github.com/sigmavirus24/github3.py ```.
- Ensure that you don't have *repositories.txt* or *code.csv* files in the directory where you want to execute the script from a previous run.

Following are the steps to execute both scripts:
1.	Open a shell to execute the Python scripts, e.g. the power shell on Windows or bash on Linux. 
4.	Update *get_matching_repositories.py* and *get_matching_code_files.py* scripts with valid GitHub username and password. Be aware that you added your credentials to these files before you commit them! 
5.  ``$ cd DIR\With\Scripts`` where *DIR\With\Scripts* is the directory which contains the both Python scripts. 
6.	To execute the first python script, run the following command:
    ```` python get_matching_repositories.py ````
This will extract Java repositories and export their information into *repositories.txt* file.
7.	To execute the second python, run the following command:
``` python get_matching_code_files.py --username <githubusername> --repoFile repositories.txt --outputFile code.csv ```
This will generate the final results in a *code.csv* file which would have the list of repositories along with the file names which are using the *javax.crypto* library.
