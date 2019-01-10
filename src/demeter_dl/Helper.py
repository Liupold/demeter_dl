from threading import Thread, _start_new_thread, Lock
from queue import Queue
from time import sleep
import logging


class LOG(object):
    """
    simple loger class return loging function as a callable instance
    init details:
        Return None, takes PRINT_DEBUG, PRINT_INFO, PRINT_WARN, PRINT_ERROR
        Parameters
        ----------
        PRINT_DEBUG(bool):
            if true debug messege will be displayed
            (default: False)
        PRINT_INFO(bool):
            if true info messege will be displayed
            (default: True)
        PRINT_WARN(bool):
            if true  warnings will be displayed
            (default: True)
        PRINT_ERROR(bool):
            if true error messege will be displayed
            (default: True)
        Returns
        -------
        None
        """

    def __init__(self, PRINT_INFO=True, PRINT_WARN=True,
                 PRINT_ERROR=True, PRINT_DEBUG=False):
        self.PRINT_DEBUG = PRINT_DEBUG
        self.PRINT_INFO = PRINT_INFO  # True if u want to monitor
        self.PRINT_ERROR = PRINT_ERROR
        self.PRINT_WARN = PRINT_WARN

    def __call__(self, code, message):
        """
        Return None,
        takes code, message
        print the nessary log
        Parameters
        ----------
        code(int):
            0: info level
            1: waring level
            2: error level
            3: debug level
        message(str):
            log message, message to be displayed
            to the user
        Returns
        -------
        None
        """
        from colorama import Fore, Back, Style
        message = str(message)
        if code == 0 and self.PRINT_INFO:
            print('[', end='')
            print(Fore.GREEN + Style.BRIGHT + 'INFO' + Style.RESET_ALL, end='')
            print('] ' + message)
        if code == 1 and self.PRINT_WARN:
            print('[', end='')
            print(Fore.YELLOW + 'WARNING' + Style.RESET_ALL, end='')
            print('] ' + message)
        if code == 2 and self.PRINT_ERROR:
            print('[', end='')
            print(Fore.RED + 'ERROR' + Style.RESET_ALL, end='')
            print('] ' + message)
        if code == 3 and self.PRINT_DEBUG:
            if self.PRINT_DEBUG:
                print(Fore.WHITE + Back.BLUE +
                      '\b[DEBUG] {}' + Style.RESET_ALL.format(message))


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] :: %(message)s",
    datefmt='%d-%b-%Y %H:%M:%S',
    filename='demeter_dl.log', level=logging.INFO)


def get_info(url):
    """
    Return final url and header For the given url

    Parameters
    ----------
    url: str
        url which will be processed

    Returns
    -------
    str, dict, bool
        redirected_url, headers, SSL_verified

    """
    from requests import get
    from requests.packages.urllib3 import disable_warnings
    from requests.exceptions import ConnectionError, MissingSchema

    dummy_headers = {'Range': 'bytes=0-100',
                     'User-Agent': 'Mozilla/5.0(X11; Linux x86_64)'}
    try:
        logging.info('Waiting for File INFO')
        dummy_request = get(
            url, headers=dummy_headers,
            stream=True)
        dummy_request.close()
        logging.info('Recived File INFO')
        # contains all the info
        recived_headers = dummy_request.headers
        final_url = dummy_request.url  # return the final url after redirecting
        return final_url, recived_headers, True

    except ConnectionError as e:
        try:
            disable_warnings()
            dummy_request = get(url, verify=False,
                                stream=True, headers=dummy_headers)
            dummy_request.close()
            logging.error('This url may contains Virus  as it\'s INSECURE')
            return dummy_request.url, dummy_request.headers, False
            logging.warning('{} May contains VIRUS'.format(url))
        except Exception:
            logging.error('get_headers[{}]: {}'.format(
                e.__traceback__.tb_lineno, e))
        return url, {}, False
    except MissingSchema:
        logging.warning('Do you mean http://{}/?'.format(url))
        return get_info('http://{}/'.format(url))
    except Exception as e:
        logging.critical('get_info[{}]: {}'.format(
            e.__traceback__.tb_lineno, e))
        raise e


def _is_downloadable(headers):
    """
        Return bool, takes dict

        returns true/false if a payload is a file other than html
        taking header(in dict form) as param

        Parameters
        ----------
        headers(dict):
            header of a payload in dict format

        Returns
        -------
        bool

        True:
            file is not html and downloadable
        False:
            fiie is a html

        """

    try:
        if 'html' not in headers['Content-Type']:
            return True
        else:
            return False
    except KeyError:
        return False

    except Exception as e:
        logging.critical('_is_downloadable[{}]: {}'.format(
            e.__traceback__.tb_lineno, e))
        raise e


def get_filename(url, headers):
    """
        Return filename(str), takes url(str), headers(dict)

        returns true/false if a payload is a file other than html
        taking header(in dict form) as param

        Parameters
        ----------
        url(str):
            url of the file

        headers(dict):
            header of a payload in dict format

        Returns
        -------

        filename(str):
            filename with file format in str

        """

    def utf_remover(string):
        if string[0:7] == "UTF-8''":
            return string[7::]
        else:
            return string

    try:
        from urllib.parse import unquote
        from time import time
        from cgi import parse_header
        if 'Content-Disposition' in headers:
            _param = parse_header(headers['Content-Disposition'])[1]
            if 'filename' in _param:
                filename = _param['filename']
                filename = filename.replace(":", " ").replace(
                    "/", "_").replace("\\", "_").replace("*", " ")
                filename = filename.replace(">", " ").replace(
                    "<", " ").replace("?", " ").replace("|", "_")
                return utf_remover(unquote(filename))
            elif 'filename*' in _param:
                filename = _param['filename*']
                filename = filename.replace(":", " ").replace(
                    "/", "_").replace("\\", "_").replace("*", " ")
                filename = filename.replace(">", " ").replace(
                    "<", " ").replace("?", " ").replace("|", "_")
                return utf_remover(unquote(filename))
            else:
                filename = unquote(
                    url.split('/')[-1]).replace('!', '').replace('?', '')
                filename = filename.replace(":", " ").replace(
                    "/", "_").replace("\\", "_").replace("*", " ")
                filename = filename.replace(">", " ").replace(
                    "<", " ").replace("?", " ").replace("|", "_")
                return filename
        else:
            filename = unquote(
                url.split('/')[-1]).replace('!', '').replace('?', '')
            filename = filename.replace(":", " ").replace(
                "/", "_").replace("\\", "_").replace("*", " ")
            filename = filename.replace(">", " ").replace(
                "<", " ").replace("?", " ").replace("|", "_")
            return filename
    except Exception as e:
        logging.critical('get_filename[{}]: {}'.format(
            e.__traceback__.tb_lineno, e))
        return 'File donwloaded @ {}'.format(int(time()))


def _is_pauseable(headers):
    """
        Return bool, takes dict

        returns true/false if a payload is a file other than html
        taking header(in dict form) as param

        Parameters
        ----------
        headers(dict):
            header of a payload in dict format

        Returns
        -------
        bool

        True:
            download can be pauseable (supports chunks)
        False:
            fiie is not pauseable

        """

    try:
        if 'Content-Length' in headers:
            if headers['Content-Length'] == '101':
                return True
    except Exception as e:
        logging.critical('_is_pauseable[{}]: {}'.format(
            e.__traceback__.tb_lineno, e))
    return False


# this is a impure function and not recomended to use outside of this project
def get_size(self):
    """ return file size """

    url, headers = self.url, self.recived_headers
    from requests import get
    try:
        return int(headers['Content-Range'].split('/')[-1])
    except KeyError:
        try:
            temp_requests = get(url, stream=True, verify=self.verify)
            temp_requests.close()
            return int(temp_requests.headers['Content-Length'])
        except KeyError:
            return None
        except Exception as e:
            logging.critical('get_size[{}]: {}'.format(
                e.__traceback__.tb_lineno, e))
    return None


def p_unit(self):
    """ convert bytes to easy to understand units

    >>>p_unit(1024)

    1.0 KB
    """

    try:
        unit_list = ["B", "KB", "MB", "GB", "TB"]
        for unit in unit_list:
            magnitude = round(self / (1024 ** unit_list.index(unit)), 3)
            if magnitude > 0 and magnitude < 1000:
                return "{} {}".format(magnitude, unit)
    except Exception as e:
        logging.critical('p_unit[{}]: {}'.format(
            e.__traceback__.tb_lineno, e))


# this is a impure function and not recomended to use outside of this project
def _download(self, _range, _id):
    from requests import get

    from os.path import getsize
    from os import remove

    def __main():
        main_request = get(
            self.url, headers={
                'Range': 'bytes={}-{}'.format(first, _range[1]),
                'User-Agent': 'Mozilla/5.0(X11; Linux x86_64)'},
            stream=True, verify=self.verify)
        with open(part_name, 'ab+') as file:
            for data in main_request.iter_content(chunk_size=4096):
                file.write(data)
                with self.update_lock:
                    self.done += len(data)
                if self.stoped:
                    break

    try:
        if self.no_of_parts == 1:
            part_name = self.location + self.file_name
        else:
            part_name = self.part_location + self.file_name + \
                '.' + str(_id) + '.hbp'
        if _range[0] != 0:
            first = _range[0] + 1
        else:
            first = _range[0]
        try:
            if self.pauseable:
                _already_done = getsize(part_name)
                self.done += _already_done
                first += _already_done
            else:
                logging.warning('Opps! Not Resumeable it\'s seems')
                remove(part_name)
        except FileNotFoundError:
            pass
        if _range[1] is not None:
            if _id == (self.no_of_parts - 1):
                if first < _range[1]:
                    __main()
            else:
                if first < (_range[1] + 1):
                    __main()

        else:
            __main()
        if not self.stoped:
            self.no_completed += 1
    except Exception as e:
        logging.critical('_download[{}]: {}'.format(
            e.__traceback__.tb_lineno, e))
        raise e


# this is a impure function and not recomended to use outside of this project
def _writer(self):
    if self.no_of_parts != 1 and self.completed:
        self._written = 0

        try:
            from os import remove
            from os.path import getsize
            if self.no_completed == self.no_of_parts:
                with open(self.location + self.file_name, 'wb') as file:
                    for _ in range(self.no_of_parts):
                        with open(self.part_location + self.file_name + '.' +
                                  str(_) + '.hbp', 'rb') as p_file:
                            for data in p_file:
                                _written = file.write(data)
                                self._written += _written

                if getsize(self.location + self.file_name) == self.size:
                    for _ in range(self.no_of_parts):
                        remove(self.part_location + self.file_name + '.' +
                               str(_) + '.hbp')
                    pass
        except Exception as e:
            logging.critical('_writer[{}]: {}'.format(
                e.__traceback__.tb_lineno, e))
            raise e


class E_Thread(object):
    """
    Think of this like a snake with multiple head. Yeah!

    You initiate the class with the function which you want to run in parallel.
    You call a function in the class which
    take the perticular args for your fuction.
    They all start as soon as you call,
    but not all you can specify how many (default is 200)
    you want to run at once,
    other wait for the completion.

    more at: https://github.com/Liupold/smart-python-thread
    """

    def __init__(self, G_THREAD, timeout=1000, Max_thread=150):
        self.G_TH = G_THREAD
        self.timeout = timeout  # will prevent from waiting for the thread
        self.TH_Q = Queue(Max_thread)     # the Queue containg threads
        self.limit = Max_thread  # maximum no. of thread that can run at once
        self.done = 0
        self.thread_no = 0
        self.run = True

        for _ in range(self.limit):
            self.TH_Q.put(Thread(target=self.G_TH, daemon=True))

    def Worker(self, X_thread, *args):  # Worker which actuall does the work
        X_thread._args = args[0]
        X_thread.start()
        X_thread.join()
        with Lock():
            self.done += 1
            self.TH_Q.put(Thread(target=self.G_TH, daemon=True))

    def start(self, *args):  # manage the work
        """ The func to be called multiple times """
        X_thread = self.TH_Q.get()
        _start_new_thread(self.Worker, (X_thread, args))
        self.thread_no += 1

    def join(self):
        while self.done != self.thread_no:
            sleep(0.0167)
        else:
            pass  # this will terminate after all thread is being completed

    def close(self):
        # will prevent further thread allocation but will not stop the ongoing
        self.done = self.thread_no
