import json
import os
from ConfigParser import ConfigParser


def read_json_from_file(filepath):
    with open(filepath, 'rb') as fp:
        dic = json.load(fp)
    return dic


def write_json_to_file(filepath, data_dict):
    with open(filepath, 'w') as fp:
        json.dump(data_dict, fp, indent=4)

def get_config_from_path(configPath, section):    
    read = False
    result = "none"
    
    #check if config file exists
    if ( os.path.isfile(configPath)):        
        config = ConfigParser();
        #try to read the value from ini file
        try:
            config.read(configPath)
            if config.has_section(section):
                params = config.items(section)   
                result = dict(params)
                read = True
        except: #read failed due currupted ini file that can happen due to suddent power of during update            
            ndutil.tprint("Error in %s file, wait till otacheck update it back " % configPath) 

    return result