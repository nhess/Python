#!/usr/bin/python3

import csv, re, json, os, argparse

def main(username):

	fileName = f'{username}_budgetSettings.json'

	# All functions in this dictionary need to have same arguments right now
	options = { 'add': addCategories, 'delete': delCategories, 'budget': None }

	try:
		with open(os.path.join("userSettings", fileName)) as f_obj:
			settings = json.load(f_obj)
		print(f"\nWelcome, {username}.  Here are your budget categories:")	

		for category, transaction in settings.items():
			print(f'\t{category}')
		print('\nWould you like to add or delete any categories?')	

		options_list = [key for key in options]
		choice = menu('Selection: ', options_list)
		
		try:
			options.get(options_list[choice])(username, fileName)
			main(username)
		except TypeError:
			pass

		csvFile = csvUserFile()		
		newSettings = newTransactions(settings, fileName, csvFile)
 
		with open(os.path.join("userSettings", fileName), 'w') as f_obj:		
			json.dump(newSettings, f_obj, indent=2, sort_keys=True)

		withdrawDict = calcWithdrawals(settings, fileName, csvFile)
		deposit = calcDeposits(settings, fileName, csvFile)	
		budget = csvBudget(deposit, withdrawDict)

		print("Calculated your budget and saved it as 'budget.csv'.")

	except FileNotFoundError:
		if username:
			pass
		else:
			username = newUser()

		fileName = f'{username}_budgetSettings.json'
		print(f"Hello, {username}!  Let's make some budget categories.")
		addCategories(username, fileName)
		main(username)

""" Get a user name from a new user """
def newUser():
	username = input('Create a username: ')
	names = os.listdir('userSettings')
	
	for name in names:
		exists = re.match(r'(.+)_budgetSettings.json', name)
		if exists.group(1) == username:
			print(f'{username} already exists. Please choose another name: ')
			return newUser()
	return username

""" A user input menu selection function """
def menu(prompt, selections):
	for index, key in enumerate(selections):
		print(f'\t{index}) {key.upper()}')

	try:
		choice = int(input(prompt))
		if not 0 <= choice < len(selections):
			raise ValueError	
	except ValueError:
		print(f'\nThat is not a valid option, please enter a number in the menu range!\n')
		return menu(prompt, selections)
		
	return choice

""" Add up all the withdrawal values from the csv file and store in a dictionary """
def calcWithdrawals(settings, fileName, csvFile):
	amount = 0
	withdrawal = {}

	for category, transactions in settings.items():
		with open(csvFile) as csv_budget:
			csv_reader = csv.DictReader(csv_budget)
			for line in csv_reader:
				for transaction in transactions:
					if transaction.lower() in (line['transaction']).lower():
						withdrawalRegex = moneyRegex(line['withdrawal'])
						amount += float(withdrawalRegex)
		withdrawal[category.strip()] = amount
		amount = 0
	return withdrawal

""" Calculate deposits from csv file """
def calcDeposits(settings, fielName, csvFile):
	amount = 0

	with open(csvFile) as csv_budget:
		csv_reader = csv.DictReader(csv_budget)
		for line in csv_reader:
			if line['deposit'] != '':
				depositRegex = moneyRegex(line['deposit'])
				amount += float(depositRegex)
	return amount

""" Set up budget categories for a first time user """
def addCategories(username, fileName):
	transactions = []

	try:
		with open(os.path.join('userSettings', fileName)) as f_obj:
			settings = json.load(f_obj)
	except FileNotFoundError:
		print(f'Welcome user {username}')
		settings = dict()

	categories = input("Enter categories separated by a comma: ").split(',')
	print('Writing the following categories to your settings:')

	for category in categories:
		print(f'    {category}', end='')
		settings[category.strip()] = transactions

	with open(os.path.join('userSettings', fileName), 'w') as f_obj:
		json.dump(settings, f_obj, indent=2, sort_keys=True)
			
""" Function to delete budget categories from json file """
def delCategories(username, fileName):
	with open(os.path.join('userSettings', fileName)) as f_obj:
		settings = json.load(f_obj)

	print('\nWhich category do you wish to delete?')

	selection = menu('Selection: ', settings)
	for index, key in enumerate(settings):
		if selection == index:
			removedValue = key

	settings.pop(removedValue)		
	print('Budget category ' + removedValue + ' was deleted from settings.')

	with open(os.path.join('userSettings', fileName), 'w') as f_obj:
		json.dump(settings, f_obj, indent=2, sort_keys=True)

	print('Would you like to delete another category?')	
	options = ['yes', 'no']
	anotherDel = menu('Selection: ', options)

	if anotherDel == 0:
		delCategories(username, fileName)
	elif anotherDel == 1:
		pass

""" Check for new transactions in csv file and return new settings 
	to be written to the json user settings file """
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
		
					transactChoice = menu('Please enter the number for the category: ', settings)
					for index, key in enumerate(settings):
						if transactChoice == index:
							json_values.append(line['transaction'])
							settings[key].append(line['transaction'])
							print('\nWriting ' + line["transaction"] + " to " + key)
	return settings

""" Get all the csv filenames in program location and ask user which csv file to use """
def csvUserFile():
	csvFiles = []

	print('\nHere are the csv files found in the working directory:')
	for filename in os.listdir('.'):
		if filename.endswith('.csv'):
			csvFiles.append(filename)
	
	csvFiles.sort(key = str.lower)
	csvChoice = menu('\nWhich csv budget file do you wish to use? ', csvFiles)
	return csvFiles[csvChoice]

""" Write the calculated values to file 'budget.csv' """
def csvBudget(deposit, withdrawDict):
	with open('budget.csv', 'w') as budgetFile:
		csvWriter = csv.writer(budgetFile)

		for key, value in withdrawDict.items():
			csvWriter.writerow([key, value])
		csvWriter.writerow(['Deposit', deposit])

""" Function to remove money symbols """
def moneyRegex(money):
	return re.sub(r"[/,/\$]", "",money)	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Budget organizer')
	parser.add_argument('-u', '--username', metavar='', help='An existing user')
	args = parser.parse_args()
	main(args.username)