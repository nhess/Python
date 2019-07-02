#!/usr/bin/python3

import csv, re, openpyxl, json
import os
import sys

def main():

	username = input("user name: ")
	filename = username + '_budgetSettings.json'

	try:
		with open('userSettings/' + filename) as f_obj:
			print("Welcome back, " + username + ".  Here are your settings:")
			settings = json.load(f_obj)
			# print(settings)
			#TODO: ask if user wishes to change settings  
			returningBudget(settings)  
	except FileNotFoundError:
		firstBudget(username, filename)

#Set up budget categories
def firstBudget(user, file):
	withdrawDict = {}
	transactions = []
	regex = re.compile(' ')

	with open('userSettings/' + file, 'w') as f_obj:
		print("Hello, " + user + "!  Let's make some budget catagories.")

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
	pass
			
def moneyRegex(money):
	""" Function to remove money symbols """
	money = re.sub(r"[/,/\$]", "",money)
	return money	

if __name__ == '__main__':
    main()