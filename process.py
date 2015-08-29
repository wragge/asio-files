import csv
from pymongo import MongoClient
from credentials import MONGOLAB_URL


def export_csv(series_id):
    dbclient = MongoClient(MONGOLAB_URL)
    db = dbclient.get_default_database()
    with open('data/{}.csv'.format(series_id), 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
                'barcode',
                'series',
                'control_symbol',
                'title',
                'start_date',
                'end_date',
                'access_status',
                'location',
                'digitised_status',
                'digitised_pages'
            ])
        for item in db.items.find({'series': series_id}):
            csv_writer.writerow([
                    item['identifier'],
                    item['series'],
                    item['control_symbol'],
                    item['title'],
                    item['contents_dates']['start_date'],
                    item['contents_dates']['end_date'],
                    item['access_status'],
                    item['location'],
                    item['digitised_status'],
                    item['digitised_pages']
                ])

