import shutil
import logging

from .step import Step
from pack_yt.setting import DOWNLOAD_DIR, VIDEOS_DIR, CAPTIONS_DIR, OUTPUT_DIR


class Postflight(Step):
    def process(self, inputs, data, utils):
        if inputs['cleanup'] == True:
            shutil.rmtree(VIDEOS_DIR)
            shutil.rmtree(CAPTIONS_DIR)
            logging.getLogger('pack_yt.yt_log').info('delete videos and captions')
