import logging

from .step import Step
from pack_yt.model.found import Found

class SeachWord(Step):
    def process(self, inputs, data, utils):

        found = []
        for YT in data:
            url = YT.url
            if not utils.get_captions_exist(url):
                logging.getLogger('pack_yt.yt_log').debug('this ' + url + 'has no captions, must check it')
                continue
            for caption in YT.captions:
                if inputs['word'] in caption:
                    time = YT.captions[caption]
                    found.append(Found(YT, caption, time))

        logging.getLogger('pack_yt.yt_log').info('searching process has completed')

        return found
