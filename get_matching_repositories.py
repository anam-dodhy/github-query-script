
'''
This script queries Github for repositories written in Java with more than 100 stars
and writes the resulting repositories to a text file.

The script currently goes from Jan. 1, 2005 to Jan. 1, 2010. Change dates according to
your needs.
'''
from github3 import login
import getpass

MONTH='12'
DAY='01'
YEAR=2016
BASE_QUERY='in:file language:java stars:>100'
SORT='stars'
ORDER='desc'

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
	commit_info = get_last_commit_info(repository_search_res.repository)
	return repository_search_res.repository.full_name + commit_info

def get_last_commit_info(repository):
	for commit in repository.commits(): #returns ShortCommit
		break
	return "---Commit URL-" + commit.html_url

def run():
	github = login('anam-dodhy', password = 'germany78645tkxel') #getpass.getpass()
	repositories = set()

	for year in range(YEAR, 2017):
		query = BASE_QUERY
		next_year = year + 1
		query += ' created:"' + str(year) + '-' + MONTH + '-' + DAY + ' .. ' + str(year + 1) + '-' + MONTH + '-' + DAY + '"'
		print query
		query_results = filter(filter_private_repos, github.search_repositories(query,SORT,ORDER)) # returns Repository sorted by stars in desc order
	   	repo_info = map(get_repo_info, query_results)
	   	print 'got: ', len(repo_info)
	   	#repositories |= set(repo_info) #this is disturbing the sort order of the repositories returned

	with open('repositories.txt', 'w') as output_file:
	   output_file.write('\n'.join(repo_info))

run()
