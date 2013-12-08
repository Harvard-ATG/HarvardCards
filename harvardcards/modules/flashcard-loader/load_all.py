import os

path_files_folder = 'flashcard-exporter/data/'
path_folder_full = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir, path_files_folder)

for file in os.listdir(path_folder_full):
    if file.endswith('.json'):
        print "Now loading " + file + "\n"
        os.system("python load_initial_data.py %s" %file)
        print "\n"
