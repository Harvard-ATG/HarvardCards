#
# The script loads the json files found in the fixtures folder into the HarvardCards Django App.
# Usage:
#   ./load_initial_data.py                      Loads the json files in the fixtures folder
#   ./load_initial_data.py [json_file]          Creates the importable json files from the given json file and then, loads them all


import os, sys
# folder where the json files are stored
path_fixtures = 'fixtures/'
script_path = os.path.dirname(os.path.abspath(__file__))

# The function loads the file into the app
def loaddata(file_name):
    file_name_full = os.path.join(script_path,path_fixtures,file_name)
    print file_name
    os.chdir(os.path.join(os.pardir, os.pardir, os.pardir))
    os.system("python manage.py loaddata %s" % file_name_full)
    os.chdir(script_path)

if len(sys.argv) == 2:
    json_file = sys.argv[1]
    if not json_file.endswith('.json'):
        print "Invalid filename."
        sys.exit()
    os.system("python initial_data.py %s" %json_file)

elif len(sys.argv) > 2:
    print "Invalid Arguments."
    sys.exit()

# load all the json files in fixtures folder
json_files = []
for file in os.listdir(path_fixtures):
    if file.endswith('.json'):
        json_files.append(file)
json_files =  sorted(json_files, key= lambda x: x.split("_")[0])

map(loaddata, json_files)