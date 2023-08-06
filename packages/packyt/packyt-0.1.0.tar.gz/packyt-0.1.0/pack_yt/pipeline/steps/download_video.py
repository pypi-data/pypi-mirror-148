from pytube import YouTube
import logging

from .step import Step
from pack_yt.setting import VIDEOS_DIR


class DownloadVideo(Step):

    def process(self, inputs, data, utils):

        yt_set = set([found.YT for found in data])
        for YT in yt_set:
            url = YT.url
            if utils.download_video_exist(url):
                logging.getLogger('pack_yt.yt_log').debug('found the same video')
                continue

            logging.getLogger('pack_yt.yt_log').debug('downloading vidoes - ')
            YouTube(url).streams.get_highest_resolution().download(output_path=VIDEOS_DIR,
                                                                   filename=utils.get_id(url) + '.mp4')
        logging.getLogger('pack_yt.yt_log').info('downloaded videos')

        return data
