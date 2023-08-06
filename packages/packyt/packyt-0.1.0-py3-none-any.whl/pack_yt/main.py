import sys
import getopt
import logging


sys.path.append('../')

from pack_yt.pipeline.pipeline import Pipeline
from pack_yt.pipeline.steps.getvideolist import GetVideoList
from pack_yt.pipeline.steps.building import Building
from pack_yt.pipeline.steps.downloadcaption import DownloadCaption
from pack_yt.utils import Utils
from pack_yt.pipeline.steps.initializeyt import InitializeYT
from pack_yt.pipeline.steps.readcaption import ReadCaption
from pack_yt.pipeline.steps.searchword import SeachWord
from pack_yt.pipeline.steps.download_video import DownloadVideo
from pack_yt.pipeline.steps.edit_video import EditVideo
from pack_yt.pipeline.steps.postflight import Postflight
from pack_yt.yt_log import yt_log


def print_usage():
    print('python main.py OPTTIONS')
    print('OPTTIONS:')
    print('{:>6} {:<20}{}'.format('-i', '--id', 'channel id of YT'))
    print('{:>6} {:<20}{}'.format('-w', '--word', 'the word we want'))
    print('{:>6} {:<20}{}'.format('-l', '--limit', 'the limit number of videos combined'))
    print('{:>6} {:<20}{}'.format('-c', '--cleanup', 'whether clean captions and video ingredients: True, False'))
    print('{:>6} {:<20}{}'.format('-s', '--stream_logger', 'level of streaming: DEBUG, INFO, WARNING, ERROR, CRITICAL'))

def main():
    inputs = {
        'channel_id': 'UCYvCbycHNeNiVOSvPhRy9lQ',
        'word': 'comparison',
        'limit': 5,
        'cleanup': False,
        'stream_logger': logging.INFO,
    }


    short_opts = 'hi:w:l:c:s:'
    long_opts = 'help id= word= limit= cleanup= stream_logger= '.split()

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ("-i", "--id"):
            inputs['channel_id'] = arg
        elif opt in ("-w", "--word"):
            inputs['word'] = arg
        elif opt in ("-l", "--limit"):
            inputs['limit'] = int(arg)
        elif opt in ("-c", "--cleanup"):
            inputs['cleanup'] = eval(arg)
        elif opt in ("-s", "--stream_logger"):
            inputs['stream_logger'] = eval(f'logging.{arg}')





    steps = [
        Building(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaption(),
        ReadCaption(),
        SeachWord(),
        DownloadVideo(),
        EditVideo(),
        Postflight(),
    ]

    utils = Utils()
    yt_log(inputs['stream_logger'])
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
