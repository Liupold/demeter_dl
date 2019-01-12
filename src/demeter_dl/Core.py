from threading import Lock, Thread
from os.path import isdir
from os.path import isfile, getsize
from os import mkdir
import logging
from .Helper import E_Thread, get_filename, get_info, get_size
from .Helper import LOG, p_unit, _download
from .Helper import _is_downloadable, _is_pauseable, _writer

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] :: %(message)s",
    datefmt='%d-%b-%Y %H:%M:%S',
    filename='demeter_dl.log', level=logging.INFO)


class HarvesterEngine(object):
    def __init__(self, url, **kargs):
        try:
            logging.info("\n\n\n\n\n\nINITIALISING:")
            self.given_url = url
            self.verify = True  # ssl verification
            self.url, self.recived_headers,\
                self.verify = get_info(
                    url)
            logging.debug('self.url@{}: {}'.format(self, self.url))
            logging.debug('self.recived_headers@{}: {}'.format(
                self, self.recived_headers))
            self.downloadable = _is_downloadable(
                self.recived_headers)
            if self.downloadable:
                self.file_name = get_filename(
                    self.url, self.recived_headers)
                self.size = get_size(self)
                logging.debug('self.size@{}: {}'.format(self, self.size))
                logging.info('FILE SIZE: {}'.format(self.size))
                self.pauseable = _is_pauseable(
                    self.recived_headers)
                logging.debug('self.pauseable@{}: {}'.format(
                    self, self.pauseable))
                logging.debug('self.pauseable@{}: {}'.format(
                    self, self.pauseable))
                self.location = ''
                self.part_location = ''
                # loaction of the temp part file during downloading
                logging.debug('self.location@{}: {}'.format(
                    self, self.location))
                self.stoped = False
                self.downloading = False
                self.completed = False
                self.done = 0
                self.block = True
                self.no_completed = 0  # how many threads completed
                self.max_alive_at_once = 8
                logging.debug('self.max_alive_at_once@{}: {}'
                              .format(
                                  self, self.max_alive_at_once))
                self.no_of_parts = 16
                logging.debug('self.no_of_parts@{}: {}'.format(
                    self, self.no_of_parts))

                # assign_karg
                if 'file_name' in kargs:
                    self.file_name = kargs.pop('file_name')
                if 'location' in kargs:
                    self.location = kargs.pop('location')
                if 'part_location' in kargs:
                    self.part_location = kargs.pop('part_location')
                if 'max_alive_at_once' in kargs:
                    self.max_alive_at_once = kargs.pop('max_alive_at_once')
                if 'no_of_parts' in kargs:
                    self.no_of_parts = kargs.pop('no_of_parts')
                if kargs != {}:
                    for parram in kargs.keys():
                        logging.error('Invalid option! "{}"'.format(parram))

                if not isdir(self.location):
                    if self.location != '':
                        mkdir(self.location)
                        logging.info(
                            '{} Directory is created'
                            .format(
                                self.location))
                if not isdir(self.part_location):
                    if self.part_location != '':
                        mkdir(self.part_location)
                        logging.info(
                            '{} Directory is created'
                            .format(
                                self.part_location))
                logging.debug('self.file_name@{}: {}'.format(
                    self, self.file_name))
                logging.info(
                    'FILE NAME: {}'
                    .format(self.file_name))

            else:
                logging.warning(1, 'Not Downloadable!')
        except Exception as e:
            logging.critical(
                'HarvesterEngine.__init__@{}[{}]: {}'
                .format(
                    self, e.__traceback__.tb_lineno, e))
            raise e

    def Download(self, blocking=True):
        """ Start The download!
            Blocking is given by the blocking param
            # default blocking is True
            self.Download(blocking=True)
        """
        def cheak_if_exist():
            # this function is only defines to used recursively
            if isfile(self.location + self.file_name):
                if getsize(self.location + self.file_name) == self.size:
                    self.done = self.size
                    self.completed = True
                    raise FileExistsError("Same File Probably Exists")
                else:
                    LOG()(1, "File with Same \
                        File Name Exists Changing File \
                        Name to :{}".format('New ' + self.file_name))
                    self.file_name = "New " + self.file_name
                    cheak_if_exist()
            else:
                pass

        cheak_if_exist()

        self.update_lock = Lock()
        self.block = blocking
        if self.downloadable and self.downloading:
            raise ValueError('Allready Downloading, self.downloading = True')

        def _Download():
            try:
                logging.debug('self.block@_Download@{}: {}'
                              .format(
                                  self, self.block))

                if self.downloadable and (not self.downloading):
                    self.downloading = True
                    logging.info('Starting Download!')
                    self.stoped = False
                    mother_thread = E_Thread(
                        _download, Max_thread=8)
                    if (not self.pauseable) or (self.size is None):
                        self.no_of_parts = 1
                        Part_length = 0
                    else:
                        Part_length = self.size // self.no_of_parts
                    logging.debug(
                        'Part_length@_Download@{}: {}'
                        .format(
                            self, Part_length))
                    for _ in range(self.no_of_parts - 1):
                        mother_thread.start(
                            self, (_ * Part_length, (_ + 1) * Part_length), _)

                    mother_thread.start(
                        self, ((self.no_of_parts - 1) *
                               Part_length, self.size),
                        self.no_of_parts - 1)

                    mother_thread.join()
                    self.completed = True
                    self.downloading = False
                    _writer(self)
                else:
                    pass

            except Exception as e:
                logging.critical(
                    'HarvesterEngine._Download@{}[{}]:\
                                     {}'.format(
                        self,
                        e.__traceback__.tb_lineno, e))
                self.downloading = False
                self.DownloadError = e
                print(e)
                mother_thread.close()

        main_thread = Thread(target=_Download, daemon=True)
        main_thread.start()
        if self.block:
            try:
                main_thread.join()
            except KeyboardInterrupt:
                self.Pause()

    def Pause(self):
        try:
            if self.pauseable and self.downloadable:
                self.stoped = True
                self.downloading = False
                logging.info('Download is Paused')
                logging.debug(
                    'self.stoped@Pause@{}: {}'.format(self, self.stoped))
            else:
                logging.error('Not Pauseable')
                logging.info('Call Stop() for exit')
        except Exception as e:
            logging.critical(
                'HarvesterEngine.Pause@{}[{}]: {}'.format(
                    self, e.__traceback__.tb_lineno, e))
            raise e

    def Stop(self):
        if self.downloadable and self.downloading:
            self.stoped = True

    def Get_done(self):
        if self.size is not None:
            return self.done / self.size
        else:
            return -1

    def Get_info(self):

        try:
            if self.size is None:
                size = 'No response from Server, None'
                p_size = ''
            else:
                size = self.size
                p_size = p_unit(size)
            _info_str = "FILE NAME     : {},".format(self.file_name)
            _info_str += "\nFILE SIZE     : {}({} Bytes),".format(p_size, size)
            _info_str += "\nTARGET        : {}".format(self.location)
        except Exception as e:
            _info_str = str(id(self))
        return _info_str

    def __repr__(self):
        _repr_str = 'Harvester${}$'.format(hex(id(self)))
        return _repr_str
