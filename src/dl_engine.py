from req_fn import get_info, get_filename, get_size, toast
from req_fn import _is_pauseable, _is_downloadable
from main_dl_fn import _download, _writer
from smart_thread import E_Thread
from threading import Lock, Thread
######
#   Made by Liupold
#
######


class OpenEngine(object):
    """docstring for OpenDownloadEngine"""

    def __init__(self, url):
        # super(OpenDownloadEngine, self).__init__()
        try:
            self.given_url = url
            self.verify = True
            self.url, self.recived_headers = get_info(self, url)
            toast(3, 'self.url@{}: {}'.format(self, self.url))
            toast(3, 'self.recived_headers@{}: {}'.format(
                self, self.recived_headers))
            self.downloadable = _is_downloadable(self.recived_headers)
            if self.downloadable:
                self.file_name = get_filename(
                    self.url, self.recived_headers, self.given_url)
                toast(3, 'self.file_name@{}: {}'.format(self, self.file_name))
                toast(0, 'recv file_name: {}'.format(self.file_name))
                self.size = get_size(self)
                toast(3, 'self.size@{}: {}'.format(self, self.size))
                toast(0, 'recv file_size: {}'.format(self.size))
                self.pauseable = _is_pauseable(self.recived_headers)
                toast(3, 'self.pauseable@{}: {}'.format(self, self.pauseable))
                toast(0, '{} Pauseable: {}'.format(
                    self.file_name, self.pauseable))
                self.location = ''
                self.part_lacation = ''
                # loaction of the temp part file during downloading
                toast(3, 'self.location@{}: {}'.format(self, self.location))
                self.paused = False
                self.downloading = False
                self.completed = False
                self.done = 0
                self.no_completed = 0  # how many threads completed
                self.max_alive_at_once = 8
                toast(3, 'self.max_alive_at_once@{}: {}'.format(
                    self, self.max_alive_at_once))
                self.no_of_parts = 16
                toast(3, 'self.no_of_parts@{}: {}'.format(
                    self, self.no_of_parts))
                self.block = True  # blocks the thread till download completes
                self.update_lock = Lock()
            else:
                pass
        except Exception as e:
            toast(2, 'OpenEngine.__init__@{}: {}'.format(self, e))

    def Donwload(self, blocking=True):
        self.block = blocking

        def _Download():
            try:
                toast(3, 'self.block@_Download@{}: {}'.format(
                    self, self.block))
                if self.downloadable:
                    toast(0, 'Starting Download!')
                    self.downloading = True
                    if (not self.pauseable) or (self.size == -1):
                        self.no_of_parts = 1
                    mother_thread = E_Thread(_download, Max_thread=8)
                    Part_length = self.size // self.no_of_parts
                    toast(3, 'Part_length@_Download@{}: {}'.format(
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
                    _writer(self)
                else:
                    pass

            except Exception as e:
                toast(2, 'OpenEngine._Download@{}: {}'.format(self, e))
            finally:
                self.downloading = False

        main_thread = Thread(target=_Download, daemon=True)
        main_thread.start()
        if self.block:
            main_thread.join()

    def Pause(self):
        try:
            if self.pauseable:
                self.paused = True
                toast(0, 'Download is Paused')
                toast(3, 'self.paused@Pause@{}: {}'.format(self, self.paused))
            else:
                toast(1, 'Not Pauseable')
        except Exception as e:
            toast(2, 'OpenEngine.Pause@{}: {}'.format(self, e))

    def Stop(self):
        pass

    def Resume(self):
        try:
            if self.pauseable and not self.downloading:
                toast(0, 'The File is Resumemed')
                toast(3, 'self.paused@Resume@{}: {}'.format(
                    self, self.paused))
                self.paused = False
            else:
                toast(1, 'The File is not Resumeable or already downloading!')
        except Exception as e:
            toast(2, 'OpenEngine.Resume@{}: {}'.format(self, e))

    def Get_done(self):
        if self.size is not None:
            return self.done / self.size
