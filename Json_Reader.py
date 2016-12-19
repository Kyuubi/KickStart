import ijson
import json

def populate(fields, prefix, value, dictionary, Dtype=1):
        check = prefix.split('.')
        if all(i in check for i in fields):
            # print "What?"
            if Dtype==0 and len(check)==len(fields):
                dictionary[value] = {}
                return True, value
            elif Dtype==1:
                dictionary[fields[-1]] = value
                # print prefix, value
            elif Dtype==2:
                if fields[-1] in dictionary.keys():
                    dictionary[fields[-1]].append(value)
                else:
                    dictionary[fields[-1]] = [value]
        return False, 0
        


def read_json_from_file(filepath):
    with open(filepath, 'rb') as fp:
        dic = json.load(fp)
    return dic


def write_json_to_file(filepath, data_dict):
    with open(filepath, 'w') as fp:
        json.dump(data_dict, fp, indent=4)


def get_value_from_ijson(parser):
    with open(filename, 'r') as fp:
        parser = ijson.parse(fp)
        return parser