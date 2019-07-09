#!/usr/bin/python3

import csv, re, openpyxl, json
import os
import sys

def main():

	username = input("user name: ")
	fileName = f'{username}_budgetSettings.json'

	try:
		with open(f'userSettings/{fileName}') as f_obj:
			print(f"Welcome back, {username}.  Here are your settings:")
			settings = json.load(f_obj)
			# print(settings)
			#TODO: ask if user wishes to change settings  
			returningBudget(settings)  
	except FileNotFoundError:
		firstBudget(username, fileName)

#Set up budget categories
def firstBudget(username, fileName):
	withdrawDict = {}
	transactions = []
	regex = re.compile(' ')

	with open(f'userSettings/{fileName}', 'w') as f_obj:
		print(f"Hello, {username}!  Let's make some budget catagories.")

		query = '\nEnter a category for your withdrawals with no spaces between words (Rent, Car_Insurance, etc.).'
		query += '  Enter q when finished: '

		while True:
			category = input(query)
			if category.lower() == 'q':
				print("These are your categories:")
				print(withdrawDict)
				json.dump(withdrawDict, f_obj, indent=2, sort_keys=True)
				break # TODO: get user to next part, organizing budget categories
			elif (regex.search(category.lower()) == None):
				withdrawDict[category] = transactions
			else:
				print('Invalid response, please enter a category with no spaces (ex. Car_Insurance).')	



#TODO: User input for adding up budget categories.
def returningBudget(settings):
	json_values = []

	with open('04-2019_bank-statement_copy.csv') as csv_budget:
		csv_reader = csv.DictReader(csv_budget) 

		for key, values in settings.items():
			for value in values:
				json_values.append(value)

		# print(json_values)

		for line in csv_reader:
			# print(line['transaction'])	
			if line['transaction'] not in json_values:
				print('Not Found:')
				print(line['transaction'] + line['withdrawal'])
	
def moneyRegex(money):
	""" Function to remove money symbols """
	money = re.sub(r"[/,/\$]", "",money)
	return money	

if __name__ == '__main__':
    main()