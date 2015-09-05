# asio-files
Code to harvest and process publicly accessible ASIO files from the National Archives of Australia.

## DIY harvesting

If you want to harvest the data yourself you'll need to clone my [recordsearch-tools](https://github.com/wragge/recordsearch_tools) repository into a direct called 'rstools'. Then in Python you can just:

````
import harvest
# Initiate harvester with a series id
harvester = harvest.SeriesClient(series='A6119')
# Harvest item metadata
harvester.do_harvest()
# Harvest ALL the digitised images in this series
harvest.harvest_images()
````

Note that harvest_images() is set up to create derivatives of every image. Just comment that out if it's not what you want.

Note too that this will work with any series in the National Archives of Australia, not just the ASIO ones!

## Here's a harvest I prepared earlier

Unless you're very keen and very patient you probably don't want to harvest everything yourself. I'm happy to make the results of my own harvests available for research.

Here's [a summary](https://github.com/wragge/asio-files/blob/master/data/series_summary.csv) of the series I've harvested.

### Metadata

Here's the basic metadata for every item saved as a CSV file:

* [A6119](https://github.com/wragge/asio-files/blob/master/data/A6119.csv)
* [A6122](https://github.com/wragge/asio-files/blob/master/data/A6122.csv)
* [A6126](https://github.com/wragge/asio-files/blob/master/data/A6126.csv)
* [A9626](https://github.com/wragge/asio-files/blob/master/data/A9626.csv)

### Images

If you'd like copies of all the images I've harvested, let me know. I'm keen to encourage further research using these files. Here are the README files for each of the image dumps:

* [README-A6119](https://github.com/wragge/asio-files/blob/master/docs/README-A6119.md)
* [README-A6122](https://github.com/wragge/asio-files/blob/master/docs/README-A6122.md)
* [README-A6126](https://github.com/wragge/asio-files/blob/master/docs/README-A6126.md)
* [README-A9626](https://github.com/wragge/asio-files/blob/master/docs/README-A9626.md)

All together there are about 300,000 images, comprising nearly 70gb of data.



