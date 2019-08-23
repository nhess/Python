#!/usr/bin/python3

import csv, re, json, os, argparse

def main(username):

	fileName = f'{username}_budgetSettings.json'

	try:
		with open(os.path.join("userSettings", fileName)) as f_obj:
			print(f"Welcome, {username}.  Here are your budget categories:")
			settings = json.load(f_obj)
			for category, transaction in settings.items():
				print(f'\t{category}')
			# TODO: ask if user wishes to change settings
			# change = input('Would you like to add any categories (y/n)? ')
		csvFile = csvUserFile()		
		newSettings = newTransactions(settings, fileName, csvFile)

		""" Take updated settings from newTransactions function 
			and save to user settings json file """  
		with open(os.path.join("userSettings", fileName), 'w') as f_obj:		
			json.dump(newSettings, f_obj, indent=2, sort_keys=True)

		withdrawDict = calcWithdrawals(settings, fileName, csvFile)
		deposit = calcDeposits(settings, fileName, csvFile)	
		budget = csvBudget(deposit, withdrawDict)

	except FileNotFoundError:
		username = newUser()
		fileName = f'{username}_budgetSettings.json'
		print(f"Hello, {username}!  Let's make some budget categories.")
		newCategories(username, fileName)
		main(username)


def newUser():
	username = input('Create a username: ')
	names = os.listdir('userSettings')
	
	for name in names:
		exists = re.match(r'(.+)_budgetSettings.json', name)
		if exists.group(1) == username:
			print(f'{username} already exists. Please choose another: ')
			return newUser()
	return username


""" Add up all the withdrawal values from the csv file and store in a dictionary. """
def calcWithdrawals(settings, fileName, csvFile):
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
						# print(line['withdrawal'] + ' ' + line['date'])
						withdrawalRegex = moneyRegex(line['withdrawal'])
						amount += float(withdrawalRegex)
		withdrawal[category.strip()] = amount
		amount = 0
		# print('\n')
	print(withdrawal)
	return withdrawal

""" Calculate deposits from csv file. """
def calcDeposits(settings, fielName, csvFile):
	amount = 0

	with open(csvFile) as csv_budget:
		csv_reader = csv.DictReader(csv_budget)
		for line in csv_reader:
			if line['deposit'] != '':
				depositRegex = moneyRegex(line['deposit'])
				amount += float(depositRegex)
	print(amount)
	return amount

def csvBudget(deposit, withdrawDict):
	with open('budget.csv', 'w') as budgetFile:
		csvWriter = csv.writer(budgetFile)

		for key, value in withdrawDict.items():
			csvWriter.writerow([key, value])

		csvWriter.writerow(['Deposit', deposit])

""" Set up budget categories for a first time user """
def newCategories(username, fileName):
	withdrawDict = {}
	transactions = []

	with open(os.path.join('userSettings', fileName), 'a') as f_obj:

		categories = input("Enter categories separated by a comma: ").split(',')
		for category in categories:
			withdrawDict[category.strip()] = transactions

		print(f'Writing the following categories to your settings: {withdrawDict}')
		json.dump(withdrawDict, f_obj, indent=2, sort_keys=True)
			
""" Check for new transactions in csv file and return new settings 
	to be written to the json user settings file. """
def newTransactions(settings, fileName, csvFile):
	json_values = []

	with open(csvFile) as csv_budget:
		csv_reader = csv.DictReader(csv_budget) 

		for key, values in settings.items():
			for value in values:
				json_values.append(value)

		for line in csv_reader:
			if line['deposit']	== '':
				if line['transaction'] not in json_values:
					print("\n********New Transaction Menu********")
					print(f'\nNot Found: {line["transaction"]}, {line["withdrawal"]}')
					print('Where should this transaction go?')
					for index, key in enumerate(settings):
						print(f'\t{index}) {key.upper()}')

					try:	
						choice = int(input('Please enter the number for the category: '))
					except ValueError:
						print(f"\nThat's not a valid option, please enter a number!")
						return newTransactions(settings, fileName, csvFile)		

					for index, key in enumerate(settings):
						if 0 > choice or choice > len(settings):
							print(f'\n{choice} is not a valid option, try again!')
							return newTransactions(settings, fileName, csvFile)
						if choice == index:
							json_values.append(line['transaction'])
							settings[key].append(line['transaction'])
					print(settings)
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
	for index, file in enumerate(csvFiles):
		print(f'\t{index}) {file}')

	try:	
		choice = int(input('\nWhich csv budget file do you wish to use? '))
	except ValueError:
		print(f"\nThat's not a valid option, please enter a number!")
		return csvUserFile()

	if 0 > choice or choice >= len(csvFiles):
		print(f'\n{choice} is not a valid option, try again!')
		return csvUserFile()
	return csvFiles[choice]

""" TODO: Add all transactions from the csvFile that appear between the json file """
def csvAddTransactions():
	pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Budget organizer')
	parser.add_argument('-u', '--username', metavar='', help='An existing user')
	args = parser.parse_args()
	main(args.username)