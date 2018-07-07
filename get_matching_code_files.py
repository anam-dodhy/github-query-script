'''
Given a list of Github repositories, this script queries those repositories
for Java code files using javax.crypto
It outputs a csv file containing the repository name and the link to the
code file
The query_size is used to avoid running into URL size limits
'''

import json
from github3 import login
import getpass
import csv
import argparse

QUERY_SIZE = 40

class CodeSearch:

	def __init__(self, username, repo_file, output_file):
		self.github = login(username, password = 'germany78645tkxel') #getpass.getpass()
		self.base_query = '"javax.crypto" language:java'
		self.repositories = []
		self.writer = None
		self.repo_file = repo_file
		self.output_file = output_file

	def read_repositories(self):
		'''
		Read list of repositories whose code will be queried
		'''
		repositories = set()
		with open(self.repo_file, 'r') as input_file:
			for repo_name in input_file:
				name,commit_url = repo_name.split("---") #each item in repositories.txt file is "repo_name---lastcommitURL"
				repositories.add(name.rstrip('\n'))
			input_file.close()

		self.repositories = list(repositories)

	def write_code_results(self, code_results):
		'''
		Given the results of the code search, write each repository and the
		matching file url to a csv file
		'''
		try:
			for code_result in code_results:
				self.writer.writerow({'repository' : code_result.repository,
					'file_url' : code_result.html_url})
		except ServerError:
		  	print "Failed"
		except ForbiddenError:
			print "Exceeded limit"

	def search_code_in_repos(self, repos):
		'''
		Appends a list of given repos to the base_query
		and uses the Github search API to search those repos
		'''
		query = self.base_query

		for repo in repos:
			query += " repo:" + repo

		return self.github.search_code(query)

	def search_code(self, start_index, end_index):
		'''
		Creates a sublist of the available repositories given the
		start and end indices, issues the query, and then writes the
		results to the csv file
		'''
		repos_to_query = self.repositories[start_index:end_index]
		code_results = self.search_code_in_repos(repos_to_query)
		self.write_code_results(code_results)


	def create_csv_file(self):
		'''
		Creates the csv file and its header
		'''
		csvfile = open(self.output_file, 'w')
		fieldnames = ['repository', 'file_url']
		self.writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
		self.writer.writeheader()

	def get_repositories(self):
		'''
		returns the available list of repos
		'''
		return self.repositories

	def get_github_obj(self):
		'''
		returns the github3 wrapper object
		'''
		return self.github

def run(username, repoFile, outputFile):
	code_search = CodeSearch(username, repoFile, outputFile)
	code_search.read_repositories()
	code_search.create_csv_file()

	num_of_repos =  len(code_search.get_repositories())
	print 'num of repos',num_of_repos
	start_index = 0
	end_index = start_index + QUERY_SIZE - 1
	if end_index > num_of_repos:
		end_index = num_of_repos - 1

	while end_index < num_of_repos:
		code_search.search_code(start_index, end_index)
		start_index += QUERY_SIZE
		end_index = start_index + QUERY_SIZE - 1

    # in case total # of repos is not divisible by the query size
	if (end_index != num_of_repos - 1):
		code_search.search_code(end_index + 1, num_of_repos - 1)


parser = argparse.ArgumentParser(description='Process repositories in repoFile and output matching code files in codeFile')
parser.add_argument('--repoFile', help='name of file containing repository list')
parser.add_argument('--outputFile', help='name of output file')
parser.add_argument('--username', help='github user name')

args = parser.parse_args()
print 'repofile', args.repoFile
print 'outputfile', args.outputFile
print 'username', args.username
run(args.username, args.repoFile, args.outputFile)
