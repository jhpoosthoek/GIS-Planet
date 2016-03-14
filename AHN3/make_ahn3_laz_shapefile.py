# Check if URL exists:
#  - https://pythonadventures.wordpress.com/2010/10/17/check-if-url-exists/
#
# AHN3 links:
#  - http://www.ahn.nl/pagina/open-data.html > http://www.ahn.nl/binaries/content/assets/hwh---ahn/common/ahn_units.zip
#  - https://www.pdok.nl/nl/ahn3-downloads
#
# Prerequisites:
#  - https://github.com/jhpoosthoek/Python-shapefile-class

from shapefile import shapefile
import httplib
import urlparse
 
def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None
 
def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes

shpfile = "ahn_units.shp"
inshp = shapefile("read", shpfile)
fieldslist = []
for line in inshp.fieldslist:
    fieldslist.append(line)
fieldslist.append(['DOWNLOAD', 4, 100])
    
outshp = shapefile("write", shpfile[:-4] + "_new.shp", inshp.type, fieldslist, inshp.projection)
for feat in inshp.features:
    attr_dict = inshp.attr_dict(feat)
    name = attr_dict["UNIT"].upper()
    url = "https://geodata.nationaalgeoregister.nl/ahn3/extract/ahn3_laz/C_%s.LAZ" % (name)
    attr_dict["DOWNLOAD"] = url
    if check_url(url):
        print url
        outshp.createfeat(feat, attr_dict)
inshp.finish()
outshp.finish()
