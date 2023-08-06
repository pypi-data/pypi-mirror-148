import os
import logging

from .step import Step
from pack_yt.setting import DOWNLOAD_DIR, VIDEOS_DIR, CAPTIONS_DIR, OUTPUT_DIR



class Building(Step):

    def process(self, inputs, data, utils):
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(CAPTIONS_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        logging.getLogger('pack_yt.yt_log').info('building dir ok')


