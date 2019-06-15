#!/usr/bin/python3

import csv, re, openpyxl

deposits = 0

wb = openpyxl.load_workbook('budget_practice_sheet.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')

def moneyRegex(money):
	""" Function to remove money symbols """
	money = re.sub(r"[/,/\$]", "",money)
	return money

with open('04-2019_bank-statement_copy.csv') as csv_budget:
	csv_reader = csv.DictReader(csv_budget)

	# Add up all deposits that have numerical values
	for line in csv_reader:
		if line['deposit'] != '':
			depositRegex = moneyRegex(line['deposit'])
			#print(depositRegex)	
			deposits += float(depositRegex)
			#print("\t" + str(deposits))

# Place deposit total and place in budget spreadsheet
sheet.cell(row=3, column=15).value = deposits
wb.save('budget_practice_sheet.xlsx')