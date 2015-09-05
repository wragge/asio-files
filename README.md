# asio-files
Code to harvest and process publicly accessible ASIO files from the National Archives of Australia.

## Harvesting

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

Note too that this will work with any series, not just the ASIO ones!



