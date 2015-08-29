from rstools.client import RSSearchClient
from pymongo import MongoClient, GEO2D
import time
import datetime
import csv
import os
import requests
from PIL import Image, ImageOps
from StringIO import StringIO

from credentials import MONGOLAB_URL

IMAGES_DIR = 'images'

IMAGE_SIZES = [(200, 200), (500, 500)]


class SeriesHarvester():
    def __init__(self, series, control=None):
        self.series = series
        self.control = control
        self.total_pages = None
        self.pages_complete = 0
        self.client = RSSearchClient()
        self.prepare_harvest()
        db = self.get_db()
        self.items = db.items

    def get_db(self):
        dbclient = MongoClient(MONGOLAB_URL)
        db = dbclient.get_default_database()
        # items = db.items
        # items.remove()
        return db

    def get_total(self):
        return self.client.total_results

    def get_db_total(self):
        return self.items.find({'series': self.series}).count()

    def prepare_harvest(self):
        if self.control:
            self.client.search(series=self.series, control=self.control)
        else:
            self.client.search(series=self.series)
        total_results = self.client.total_results
        print '{} items'.format(total_results)
        self.total_pages = (int(total_results) / self.client.results_per_page) + 1
        print self.total_pages

    def start_harvest(self, page=None):
        if not page:
            page = self.pages_complete + 1
        while self.pages_complete < self.total_pages:
            if self.control:
                response = self.client.search(series=self.series, page=page, control=self.control)
            else:
                response = self.client.search(series=self.series, page=page, sort='9')
            self.items.insert_many(response['results'])
            self.pages_complete += 1
            page += 1
            print '{} pages complete'.format(self.pages_complete)
            time.sleep(1)

    def harvest_images(self):
        db = self.get_db()
        items = db.items.find({'series': self.series, 'digitised_status': True})
        images = db.images
        headers = {'User-Agent': 'Mozilla/5.0'}
        for item in items:
            directory = os.path.join(IMAGES_DIR, '{}/{}-[{}]'.format(self.series.replace('/', '-'), item['control_symbol'].replace('/', '-'), item['identifier']))
            if not os.path.exists(directory):
                os.makedirs(directory)
                os.makedirs(os.path.join(directory, 'thumbs'))
            for page in range(1, item['digitised_pages'] + 1):
                filename = '{}/{}-p{}.jpg'.format(directory, item['identifier'], page)
                print '{}, p. {}'.format(item['identifier'], page)
                if not os.path.exists(filename):
                    img_url = 'http://recordsearch.naa.gov.au/NaaMedia/ShowImage.asp?B={}&S={}&T=P'.format(item['identifier'], page)
                    response = requests.get(img_url, headers=headers, stream=True)
                    response.raise_for_status()
                    try:
                        image = Image.open(StringIO(response.content))
                    except:
                        print 'Not an image'
                    else:
                        width, height = image.size
                        image.save(filename)
                        del response
                        image_meta = {
                            'item_id': item['_id'],
                            'identifier': item['identifier'],
                            'page': page,
                            'width': width,
                            'height': height
                            }
                        images.save(image_meta)
                        print 'Image saved'
                        for size in IMAGE_SIZES:
                            new_width, new_height = size
                            thumb_file = '{}/thumbs/{}-p{}-{}-sq.jpg'.format(directory, item['identifier'], page, new_width)
                            thumb_image = ImageOps.fit(image, size, Image.ANTIALIAS)
                            thumb_image.save(thumb_file)
                        thumb_file = '{}/thumbs/{}-p{}-200.jpg'.format(directory, item['identifier'], page)
                        thumb_image = image.copy()
                        thumb_image.thumbnail((200, 200))
                        thumb_image.save(thumb_file)
                        image.close()
                        thumb_image.close()
                    time.sleep(5)


def harvest_all_series():
    for series in SERIES_LIST:
        print 'Series {}'.format(series['series'])
        if series['range']:
            for symbol in range(series['range'][0], series['range'][1]):
                print 'Control symbol {}'.format(symbol)
                harvester = SeriesHarvester(series=series['series'], control='*{}/*'.format(symbol))
                harvester.start_harvest()
        else:
            harvester = SeriesHarvester(series=series['series'])
            harvester.start_harvest()


def get_db_items():
    dbclient = MongoClient(MONGOLAB_URL)
    db = dbclient.get_default_database()
    items = db.items
    #items.remove()
    return items


def delete_one_series(series):
    items = get_db_items()
    deleted = items.delete_many({'series': series})
    print '{} items deleted'.format(deleted.deleted_count)


def change_to_int():
    items = get_db_items()
    for record in items.find({'digitised_pages': {'$ne': 0}}).batch_size(30):
        record['digitised_pages'] = int(record['digitised_pages'])
        items.save(record)


def series_summary():
    items = get_db_items()
    with open('data/series_summary.csv', 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['series', 'total described', 'total digitised', 'percentage digitised', 'total pages digitised'])
        for series in SERIES_LIST:
            total = items.count({'series': series['series']})
            total_digitised = items.count({'series': series['series'], 'digitised_status': True})
            pipe = [{"$match": {"series": series['series']}}, {"$group": {"_id": "$series", "total": {"$sum": "$digitised_pages"}}}]
            total_pages = items.aggregate(pipeline=pipe).next()['total']
            print series['series']
            print 'Total: {}'.format(total)
            print 'Total digitised: {} ({:.2f}%)'.format(total_digitised, (total_digitised / float(total) * 100))
            print 'Total digitised pages: {}'.format(total_pages)
            csv_writer.writerow([series['series'], total, total_digitised, '{:.2f}%'.format(total_digitised / float(total) * 100), total_pages])
