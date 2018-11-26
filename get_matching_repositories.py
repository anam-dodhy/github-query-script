
'''
This script queries Github for repositories written in Java with more than 100 stars and 100 commits
and writes the resulting repositories to a text file.

The script currently provides two methods, one to get repositories for a given single year and the other one to get repositories for multiple years.
'''
from github3 import login
import getpass

START_MONTH='07'
END_MONTH='09'
DAY='01'
YEAR=2015
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
	return str(INDEX) + ";" + str(filtered_repo_info["repo_name"]) + ";" + str(filtered_repo_info["commit_count"]) + ";" + str(filtered_repo_info["commit_url"])

def get_single_year_data(base_query, year, start_month, day, end_month, sort, order, github):
	#-----------#get data for a single YEAR--------------------
	query = base_query
	query += ' created:"' + str(year) + '-' + start_month + '-' + day + ' .. ' + str(year) + '-' + end_month + '-' + day + '"'
	print query
	query_results = filter(filter_private_repos, github.search_repositories(query, sort, order)) # returns Repository sorted by stars in desc order
	return map(get_repo_info, query_results)

def get_multiple_year_data(base_query, start_year, start_month, day, end_month, sort, order, github):
	#-----------#get data for a multiple YEARS--------------------
	for year in range(start_year, 2018):
		query = base_query
		next_year = year + 1
		query += ' created:"' + str(year) + '-' + start_month + '-' + day + ' .. ' + str(year + 1) + '-' + end_month + '-' + day + '"'
		print query
		query_results = filter(filter_private_repos, github.search_repositories(query, sort, order)) # returns Repository sorted by stars in desc order
	   	repo_infos = map(get_repo_info, query_results)
		print repo_infos
	#-------------------------------
	return repo_infos

def run():
	github = login('a-dodhy', password = 'germany78645tkxel') #anam-dodhy,password=germany78645tkxel #getpass.getpass()

	repo_infos = get_single_year_data(BASE_QUERY, YEAR, START_MONTH, DAY, END_MONTH, SORT, ORDER, github)
	#repo_infos = get_multiple_year_data(BASE_QUERY, YEAR, START_MONTH, DAY, END_MONTH, SORT, ORDER)

	filtered_repo_infos = filter(get_filtered_repo, repo_infos)
	print 'got: ', len(filtered_repo_infos)

	with open('repositories.txt', 'w') as output_file:
	   output_file.write('\n'.join(map(get_result, filtered_repo_infos)))

run()
