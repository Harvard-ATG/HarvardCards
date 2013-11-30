import os, sys

if len(sys.argv) == 2:
    if sys.argv[1]=='create':
        os.system("python initial_data.py")
    else:
        print "Invalid Command."
        sys.exit()

elif len(sys.argv) == 3:
    json_file = sys.argv[2]
    if not json_file.endswith('.json'):
        print "Invalid filename."
        sys.exit()
    os.system("python initial_data.py %s" %json_file)


def loaddata(file):
    if os.path.splitext(file)[1] == '.json':
        print file
        os.system("python manage.py loaddata %s" % file)


path_fixtures = 'harvardcards/apps/flash/fixtures/'

json_files = []

for file in os.listdir(path_fixtures):
    if file.endswith('.json'):
        json_files.append(file)
json_files =  sorted(json_files, key= lambda x: x.split("_")[0])

files = []
for i in range(0, len(json_files)):
    files.append(os.path.join(os.path.dirname(__file__),path_fixtures,json_files[i]))

map(loaddata, files)