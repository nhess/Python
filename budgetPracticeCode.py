import csv, re

with open('04-2019_bank-statement_copy.csv') as csv_budget:
	csv_reader = csv.DictReader(csv_budget)

	deposits = 0

	#TODO: take the 'deposit' keys that have a value and add them all up
	for line in csv_reader:
		d = line['deposit']
		if d != '':
			currencyRegex = re.sub(r"[/,/\$]", "",d)
			print(currencyRegex)
			deposits += float(currencyRegex)
			print(deposits)
