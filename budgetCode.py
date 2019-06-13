import csv, re

with open('04-2019_bank-statement_copy.csv') as csv_budget:
	csv_reader = csv.DictReader(csv_budget)

	deposits = 0

	#TODO: take the 'deposit' keys that have a value and add them all up
	for line in csv_reader:
		if line['deposit'] != '':
			currencyRegex = re.sub(r"[/,/\$]", "",line['deposit'])
			print(currencyRegex)
			deposits += float(currencyRegex)
			print("\t" + str(deposits))
