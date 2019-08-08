#!/usr/bin/python3

import csv, re, openpyxl, json
import os
import sys

def main():

	username = input("user name: ")
	fileName = f'{username}_budgetSettings.json'

	try:
		with open(f'userSettings/{fileName}') as f_obj:
			print(f"Welcome back, {username}.  Here are your budget categories:")
			settings = json.load(f_obj)
			for category, transaction in settings.items():
				print(f'\t{category}')
			# TODO: ask if user wishes to change settings
			# change = input('Would you like to add any categories (y/n)? ')
		csvFile = csvUserFile()		
		newSettings = newTransactions(settings, fileName, csvFile)

		""" Take updated settings from newTransactions function 
			and save to user settings json file """  
		with open(f'userSettings/{fileName}', 'w') as f_obj:		
			json.dump(newSettings, f_obj, indent=2, sort_keys=True)


		budgetDict = calcBudget(settings, fileName, csvFile)	

	except FileNotFoundError:
		print(f"Hello, {username}!  Let's make some budget catagories.")
		newCategories(username, fileName)
t

""" Add up all the withdrawal values from the csv file and store in a dictionary. """
def calcBudget(settings, fileName, csvFile):
	amount = 0
	withdrawal = {}

	for category, transactions in settings.items():
		# print(category)
		# print(transactions)
		with open(csvFile) as csv_budget:
			csv_reader = csv.DictReader(csv_budget)
			for line in csv_reader:
				for transaction in transactions:
					if transaction.lower() in (line['transaction']).lower():
						# print(line['withdrawal'])
						withdrawalRegex = moneyRegex(line['withdrawal'])
						amount += float(withdrawalRegex)
		withdrawal[category.strip()] = amount
		amount = 0
		# print('\n')
	print(withdrawal)


""" Set up budget categories for a first time user """
def newCategories(username, fileName):
	withdrawDict = {}
	transactions = []

	with open(f'userSettings/{fileName}', 'a') as f_obj:

		categories = input("Enter categories separated by a comma: ").split(',')
		# print(categories)
		for category in categories:
			withdrawDict[category.strip()] = transactions

		print(f'Writing the following categories to your settings: {withdrawDict}')
		json.dump(withdrawDict, f_obj, indent=2, sort_keys=True)
			
""" Check for new transactions in csv file and return new settings 
	to be written to the json user settings file. """
def newTransactions(settings, fileName, csvFile):
	json_values = []
	# csvFile = csvUserFile()

	with open(csvFile) as csv_budget:
		csv_reader = csv.DictReader(csv_budget) 

		for key, values in settings.items():
			for value in values:
				json_values.append(value)

		for line in csv_reader:
			if line['deposit']	== '':
				if line['transaction'] not in json_values:
					print("********New Transaction Menu********")
					print(f'\nNot Found: {line["transaction"]}, {line["withdrawal"]}')
					print('Where should this transaction go?')
					for key, values in settings.items():
						print(f'\t{key.upper()}')
					choice = input('Please type the exact category: ')
					for key, values in settings.items():
						if choice.lower() == key.lower():
							json_values.append(line['transaction'])
							settings[key].append(line['transaction'])
	return settings

""" Function to remove money symbols """
def moneyRegex(money):
	money = re.sub(r"[/,/\$]", "",money)
	return money	

""" Get all the csv filenames in program location and ask user which csv file to use."""
def csvUserFile():
	print('\nHere are the csv files found in the working directory:')
	csvFiles = []
	for filename in os.listdir('.'):
		if filename.endswith('.csv'):
			csvFiles.append(filename)
			csvFiles.sort(key = str.lower)
	for file in csvFiles:
		print(f'\t{file}')

	csvBudgetFile = input('\nWhich csv budget file do you wish to use? ')
	return csvBudgetFile

""" TODO: Add all transactions from the csvFile that appear between the json file """
def csvAddTransactions():
	pass

if __name__ == '__main__':
    main()