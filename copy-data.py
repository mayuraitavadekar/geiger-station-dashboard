import shutil

source_path = "/home/geiger/Desktop/geiger/data-v1.csv"
dest_path = "/home/geiger/Desktop/dashboard/static/data-v1.csv"

# truncate all the data from dest_path
f = open(dest_path, 'w+')
f.close()

# now get the data from source csv file to dest file
shutil.copyfile(source_path, dest_path)

# completed
		

	


