
'''
This script queries Github for repositories written in Java with more than 100 stars
and writes the resulting repositories to a text file.

The script currently goes from Jan. 1, 2005 to Jan. 1, 2010. Change dates according to
your needs.
'''
from github3 import login
import getpass

START_MONTH='01'
END_MONTH='06'
DAY='01'
YEAR=2017
BASE_QUERY='in:file language:java stars:>100'
SORT='stars'
ORDER='desc'
INDEX=0

def filter_private_repos(repository_search_res):
	'''
	Filter function to remove private repos
	'''
	return not repository_search_res.repository.private

def get_repo_info(repository_search_res):
	'''
	Returns the full name of a given RepositorySearchResult
	This includes the username to include
	Change to name if you do not want the username
	'''
	commit_info = get_commit_info(repository_search_res.repository)
	return	{
			"repo_name" : repository_search_res.repository.full_name,
			"commit_count" : commit_info["count"],
			"commit_url" : commit_info["last_commit_url"]}

def get_commit_info(repository):
	for commit in repository.commits(): #returns ShortCommit (this is to get the latest commit of the rep)
		break
	latest_commit_url=commit.html_url
	commit_count = 0
	for comm in repository.commits(): #returns ShortCommit (this is to get the total commit count of the rep)
		commit_count = commit_count + 1

	return	{
			"last_commit_url" : latest_commit_url,
			"count" : commit_count}

def get_filtered_repo(repo_info):
	return repo_info["commit_count"] > 100 #filtering repositories with number of commits greater than 100

def get_result(filtered_repo_info):
	global INDEX
	INDEX = INDEX + 1
	return str(INDEX) + "---" + str(filtered_repo_info["repo_name"]) + "---" + str(filtered_repo_info["commit_count"]) + "---" + str(filtered_repo_info["commit_url"])

def run():
	github = login('a-dodhy', password = 'germany78645tkxel') #anam-dodhy,password=germany78645tkxel #getpass.getpass()

	#-----------#get data for a single YEAR--------------------
	query = BASE_QUERY
	query += ' created:"' + str(YEAR) + '-' + START_MONTH + '-' + DAY + ' .. ' + str(YEAR) + '-' + END_MONTH + '-' + DAY + '"'
	print query
	query_results = filter(filter_private_repos, github.search_repositories(query,SORT,ORDER)) # returns Repository sorted by stars in desc order
	repo_infos = map(get_repo_info, query_results)
	filtered_repo_infos = filter(get_filtered_repo, repo_infos)
	print 'got: ', len(filtered_repo_infos)

	#-----------#get data for a multiple YEARS--------------------
	#for year in range(YEAR, 2018):
		#query = BASE_QUERY
		#next_year = year + 1
		#query += ' created:"' + str(year) + '-' + START_MONTH + '-' + DAY + ' .. ' + str(year + 1) + '-' + END_MONTH + '-' + DAY + '"'
		#print query
		#query_results = filter(filter_private_repos, github.search_repositories(query,SORT,ORDER)) # returns Repository sorted by stars in desc order
	   	#repo_infos = map(get_repo_info, query_results)
		#print repo_infos
		#filtered_repo_infos = filter(get_filtered_repo, repo_infos)
	   	#print 'got: ', len(filtered_repo_infos)
	#-------------------------------

	with open('repositories.txt', 'w') as output_file:
	   output_file.write('\n'.join(map(get_result, filtered_repo_infos)))

run()
