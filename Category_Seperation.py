import support
import glob
import ijson
import json
import Json_Reader as jerry
Cat_dict = {}
Cur_types = []
Cur_conv = jerry.read_json_from_file('Currency_Conversion.json')

Project_initiation = ["item","projects","item","id"]
Static_Field_Requriments = [["projects", "name" ,"location"], 
                    ["projects", "currency"], ["projects", "name", "category"]]
Recurring_Field_Requirments = [["projects", "pledged"], ["projects", "backers_count"], 
                    ["projects", "deadline"], ["projects", "state_changed_at"],
                    ["projects", "created_at"], ["projects", "launched_at"]]

      # "deadline": 1399293386,
      # "state_changed_at": 1397133386,
      # "created_at": 1396672480,
      # "launched_at": 1397133386,



def currencyconvert(Ctype, amount):
    factor = Cur_conv[Ctype]
    return amount*factor

def json_load(filename):
    with open(filename, 'r') as fp:
        parser = ijson.parse(fp)
        flag_set=0
        # for i in parser:
        #   print i
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

def json_load_2(filename, List):
    with open(filename, 'r') as fp:
        parser = ijson.parse(fp)
        LastValue = 0
        count =0
        for prefix, event, value in parser:
            # print parser
            if event=='number':
                value = float(value)
                if value==int(value):
                    value = int(value)
            # print prefix, event, value
            state, id_num = jerry.populate(Project_initiation, prefix, value, List, Dtype = 0)
            if state == True:
                LastValue = id_num
                count = count +1
                if count%1000 == 0:

                    print count
                    # break
                if count%10000 == 0:
                    jerry.write_json_to_file('Temp_Summary.json', File_Dict)

                # print LastValue
            if LastValue in List.keys():
                for j in Static_Field_Requriments:
                    jerry.populate(j, prefix, value, List[LastValue], Dtype = 1)
                for j in Recurring_Field_Requirments:
                    jerry.populate(j, prefix, value, List[LastValue], Dtype = 2)

            


DatasetPath = support.get_config("GlobalSettings", "datasetloc")
files = glob.glob(DatasetPath+'*.json')
File_Dict = {}
for i in files:
    File_Dict[i] = {}
    json_load_2(i, File_Dict[i])

# print File_Dict
jerry.write_json_to_file('Temp_Summary.json', File_Dict)