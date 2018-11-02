from harvester import HarvesterHelper
from threading import Lock, Thread
from os.path import isdir
from os import mkdir


class HarvesterEngine(object):
    def __init__(self, url, **kargs):
        try:
            if 'print_info' in kargs:
                PRINT_INFO = kargs.pop('print_info')
                self._HarvesterCoreLOGer = HarvesterHelper.LOG(
                    PRINT_INFO=PRINT_INFO)
            else:
                self._HarvesterCoreLOGer = HarvesterHelper.LOG()
            self.given_url = url
            self.verify = True
            self.url, self.recived_headers,\
                self.verify = HarvesterHelper.get_info(
                    url)
            self._HarvesterCoreLOGer(3, 'self.url@{}: {}'
                                     .format(self, self.url))
            self._HarvesterCoreLOGer(3, 'self.recived_headers@{}: {}'.format(
                self, self.recived_headers))
            self.downloadable = HarvesterHelper._is_downloadable(
                self.recived_headers)
            if self.downloadable:
                self.file_name = HarvesterHelper.get_filename(
                    self.url, self.recived_headers)
                self.size = HarvesterHelper.get_size(self)
                self._HarvesterCoreLOGer(
                    3, 'self.size@{}: {}'.format(self, self.size))
                self._HarvesterCoreLOGer(0, 'FILE SIZE: {}'.format(self.size))
                self.pauseable = HarvesterHelper._is_pauseable(
                    self.recived_headers)
                self._HarvesterCoreLOGer(
                    3, 'self.pauseable@{}: {}'.format(self, self.pauseable))
                self._HarvesterCoreLOGer(3, 'self.pauseable@{}: {}'.format(
                    self, self.pauseable))
                self.location = ''
                self.part_location = ''
                # loaction of the temp part file during downloading
                self._HarvesterCoreLOGer(
                    3, 'self.location@{}: {}'.format(self, self.location))
                self.stoped = False
                self.downloading = False
                self.completed = False
                self.done = 0
                self.block = True
                self.no_completed = 0  # how many threads completed
                self.max_alive_at_once = 8
                self._HarvesterCoreLOGer(3, 'self.max_alive_at_once@{}: {}'
                                         .format(
                                             self, self.max_alive_at_once))
                self.no_of_parts = 16
                self._HarvesterCoreLOGer(3, 'self.no_of_parts@{}: {}'.format(
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
                        self._HarvesterCoreLOGer(
                            2, 'Invalid option! "{}"'.format(parram))

                if not isdir(self.location):
                    if self.location != '':
                        mkdir(self.location)
                        self._HarvesterCoreLOGer(0,
                                                 '{} Directory is created'
                                                 .format(
                                                     self.location))
                if not isdir(self.part_location):
                    if self.part_location != '':
                        mkdir(self.part_location)
                        self._HarvesterCoreLOGer(0,
                                                 '{} Directory is created'
                                                 .format(
                                                     self.part_location))
                self._HarvesterCoreLOGer(
                    3, 'self.file_name@{}: {}'.format(self, self.file_name))
                self._HarvesterCoreLOGer(0,
                                         'FILE NAME: {}'
                                         .format(self.file_name))
            else:
                self._HarvesterCoreLOGer(2, 'Not Downloadable!')
        except Exception as e:
            self._HarvesterCoreLOGer(2,
                                     'HarvesterEngine.__init__@{}[{}]: {}'
                                     .format(
                                         self, e.__traceback__.tb_lineno, e))

    def Download(self, blocking=True):
        """ Start The download!
            Blocking is given by the blocking param
            # default blocking is True
            self.Download(blocking=True)
        """
        self.update_lock = Lock()
        self.block = blocking

        def _Download():
            try:
                self._HarvesterCoreLOGer(3, 'self.block@_Download@{}: {}'
                                         .format(
                                             self, self.block))
                if self.downloadable and (not self.downloading):
                    self._HarvesterCoreLOGer(0, 'Starting Download!')
                    self.stoped = False
                    self.downloading = True
                    mother_thread = HarvesterHelper.E_Thread(
                        HarvesterHelper._download, Max_thread=8)
                    if (not self.pauseable) or (self.size is None):
                        self.no_of_parts = 1
                        Part_length = 0
                    else:
                        Part_length = self.size // self.no_of_parts
                    self._HarvesterCoreLOGer(3,
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
                    HarvesterHelper._writer(self)
                else:
                    raise AttributeError(
                        'Allready Downloading, self.downloading = True')

            except Exception as e:
                self._HarvesterCoreLOGer(2,
                                         'HarvesterEngine._Download@{}[{}]:\
                                     {}'.format(
                                             self,
                                             e.__traceback__.tb_lineno, e))
            finally:
                self.downloading = False

        main_thread = Thread(target=_Download, daemon=True)
        main_thread.start()
        if self.block:
            main_thread.join()
            pass

    def Pause(self):
        try:
            if self.pauseable and self.downloadable:
                self.stoped = True
                self.downloading = False
                self._HarvesterCoreLOGer(0, 'Download is Paused')
                self._HarvesterCoreLOGer(
                    3, 'self.stoped@Pause@{}: {}'.format(self, self.stoped))
            else:
                self._HarvesterCoreLOGer(1, 'Not Pauseable')
                self._HarvesterCoreLOGer(0, 'Call Stop() for exit')
        except Exception as e:
            self._HarvesterCoreLOGer(2,
                                     'HarvesterEngine.Pause@{}[{}]: {}'.format(
                                         self, e.__traceback__.tb_lineno, e))

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
                p_size = HarvesterHelper.p_unit(size)
            _info_str = "FILE NAME     : {},".format(self.file_name)
            _info_str += "\nFILE SIZE     : {}({} Bytes),".format(p_size, size)
            _info_str += "\nTARGET        : {}".format(self.location)
        except Exception as e:
            _info_str = str(id(self))
        return _info_str

    def __repr__(self):
        _repr_str = 'Harvester${}$'.format(hex(id(self)))
        return _repr_str
