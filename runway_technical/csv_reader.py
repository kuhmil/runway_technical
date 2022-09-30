import csv
import pandas as pd    

        
def csv_reader(data):
    with open('reviews.csv','a') as fd:
        write = csv.writer(fd)   
        write.writerow(data)

def csv_header(filename):
    """Create GCP csv header"""

    field_names = ['title',  'author', 'time_stamp_utc', 'version', 'rating', 'review', 'vote_count']
    f = open(filename, 'w')
    writer = csv.writer(f)
    writer.writerow(field_names)
    f.close()