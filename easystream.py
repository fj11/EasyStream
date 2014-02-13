from src import HLStreamer
from optparse import OptionParser

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-o', '', dest='vod', help='enable hls service for vod',
                      metavar='VOD')
    parser.add_option('-u', '', dest='url', help='enable hls service for live',
                      metavar='URL')
    options, args = parser.parse_args()
    if options.vod:
        hls_vod = HLStreamer.VOD()
    if options.url:
        hls_live = HLStreamer.LIVE()
        hls_live.reciveUnicastUDP(options.url)
