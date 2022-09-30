import csv
import pandas as pd    

        
def csv_reader(data):
    with open('reviews.csv','a') as fd:
        write = csv.writer(fd)   
        write.writerow(data)

def csv_header(filename):
    """Create csv header"""

    field_names = ['title', 'time_stamp_utc', 'rating', 'review', 'vote_count']
    f = open(filename, 'w')
    writer = csv.writer(f)
    writer.writerow(field_names)
    f.close()

def csv_check(file_path, message):
    df = pd.read_csv(file_path)
    if df.empty == True:
        csv_reader(message)