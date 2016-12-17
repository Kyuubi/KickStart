import support
import glob
import ijson
import json

Cat_dict = {}
Cur_types = []
Cur_conv = support.read_json_from_file('Currency_Conversion.json')
def currencyconvert(Ctype, amount):
	factor = Cur_conv[Ctype]
	return amount*factor

def json_load(filename):
	with open(filename, 'r') as fp:
		parser = ijson.parse(fp)
		flag_set=0
		# for i in parser:
		# 	print i
		pledge = -1
		for prefix, event, value in parser:
			if prefix.endswith('.pledged'):
				if pledge == -1:
					pledge = float(value)
				else:
					print "Last value still not flushed out..."
			if prefix.endswith('.currency'):
				if value not in Cur_types:
					Cur_types.append(value)
					print "Currency = ", value

			if prefix.endswith('.category.name'):
				# flag_set=0
				if value not in Cat_dict.keys():
					Cat_dict[value] = {}
					Cat_dict[value]["Count"] = 1
					Cat_dict[value]["TotalPledges"] = pledge
					Cat_dict[value]["AveragePledge"] = pledge
					pledge = -1

					# print "Category Type = ",value
				else:
					Cat_dict[value]["Count"] = Cat_dict[value]["Count"]+1
					Cat_dict[value]["TotalPledges"] = Cat_dict[value]["TotalPledges"]+pledge
					Cat_dict[value]["AveragePledge"] = (Cat_dict[value]["AveragePledge"]*(Cat_dict[value]["Count"]-1) + pledge)/float(Cat_dict[value]["Count"])
					pledge = -1


	for key,value in Cat_dict.iteritems():
		print key," = ", value


DatasetPath = support.get_config("GlobalSettings", "datasetloc")
files = glob.glob(DatasetPath+'*.json')
for i in files:
	json_load(i)

support.write_json_to_file('Category_Summary.json', Cat_dict)