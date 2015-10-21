import os, json
path_files_folder = 'apps/flash/fixtures/'
path_folder_full = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir, os.pardir, path_files_folder)

# dumps the current django data
app_name = 'flash'
filename = 'initial_data.json'
filename = path_folder_full + filename
os.chdir(os.path.join(os.pardir, os.pardir, os.pardir))
cmd = "python manage.py dumpdata --indent=4 " + app_name +">" + filename
os.system(cmd)
print "Successfully created a fixture with all the data from the app " + app_name + ".\n"