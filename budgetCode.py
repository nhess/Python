#!/usr/bin/python3

import csv, re, openpyxl

deposits = 0

withdrawals = {'rent': 0, 'studio_rent': 50, 'utilities': 0,
				'internet': 0, 'student_loan': 0, 'gym': 0,
				'car_insurance': 0, 'gas': 0, 'misc_monthly': 0,
				'groceries': 0, 'dine_out': 0, 'misc_expenses': 0		
				}

gyms = ['gym', 'fitness']
gas_stations = ['kwik trip', 'mobil']
misc_month = ['netflix', 'audible']
dining = ['monks', 'mings', 'daisy burgers', 'the mac shack', 'subs', 'chipotle']
other_expenses = ['guitar center', 'vudu', 'humblebundle']

wb = openpyxl.load_workbook('budget_practice_sheet.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')

def moneyRegex(money):
	""" Function to remove money symbols """
	money = re.sub(r"[/,/\$]", "",money)
	return money

with open('04-2019_bank-statement_copy.csv') as csv_budget:
	csv_reader = csv.DictReader(csv_budget)

	
	for line in csv_reader:
		# Add up all deposits that have numerical values
		if line['deposit'] != '':
			depositRegex = moneyRegex(line['deposit'])
			deposits += float(depositRegex)

		# Add up all withdrawals that have numerical values
		# TODO: Clean this up	
		if 'hy vee' in (line['transaction']).lower():
			withdrawalRegex = moneyRegex(line['withdrawal'])
			withdrawals['groceries'] += float(withdrawalRegex)
		if 'rent' in (line['transaction']).lower():
			withdrawalRegex = moneyRegex(line['withdrawal'])
			withdrawals['rent'] += float(withdrawalRegex)
		if 'utilities' in (line['transaction']).lower():
			withdrawalRegex = moneyRegex(line['withdrawal'])
			withdrawals['utilities'] += float(withdrawalRegex)
		if 'internet' in (line['transaction']).lower():
			withdrawalRegex = moneyRegex(line['withdrawal'])
			withdrawals['internet'] += float(withdrawalRegex)
		if 'student loan' in (line['transaction']).lower():
			withdrawalRegex = moneyRegex(line['withdrawal'])
			withdrawals['student_loan'] += float(withdrawalRegex)
		for gym in gyms:
			if gym in (line['transaction']).lower():
				withdrawalRegex = moneyRegex(line['withdrawal'])
				withdrawals['gym'] += float(withdrawalRegex)
		if 'insurance' in (line['transaction']).lower():
			withdrawalRegex = moneyRegex(line['withdrawal'])
			withdrawals['car_insurance'] += float(withdrawalRegex)
		for gas_station in gas_stations:	
			if gas_station in (line['transaction']).lower():
				withdrawalRegex = moneyRegex(line['withdrawal'])
				withdrawals['gas'] += float(withdrawalRegex)
		for misc in misc_month:		
			if misc in (line['transaction']).lower():
				withdrawalRegex = moneyRegex(line['withdrawal'])
				withdrawals['misc_monthly'] += float(withdrawalRegex)
		for dine in dining:
			if dine in (line['transaction']).lower():
				withdrawalRegex = moneyRegex(line['withdrawal'])
				withdrawals['dine_out'] += float(withdrawalRegex)
		for other in other_expenses:
			if other in (line['transaction']).lower():
				rentRegex = moneyRegex(line['withdrawal'])
				withdrawals['misc_expenses'] += float(rentRegex)

# Take deposit total and place in budget spreadsheet
sheet.cell(row=3, column=15).value = deposits
wb.save('budget_practice_sheet.xlsx')

# Save total withdrawals values in budget spreadsheet
# TODO: Clean this up
x = 2
if x < 14:
	for v in withdrawals.values():
		print(v)
		sheet.cell(row=3, column=x).value = v
		wb.save('budget_practice_sheet.xlsx')
		x += 1