def toast(code, message):
    """beutiful printer """
    PRINT_DEBUG = False
    PRINT_INFO = False
    from colorama import Fore, Back, init, Style
    from time import time
    init(autoreset=True)
    message = str(message)
    if code == 0 and PRINT_INFO:
        print('[', end='')
        print(Fore.GREEN + Style.BRIGHT + 'INFO', end='')
        print('] ' + message)
    if code == 1:
        print('[', end='')
        print(Fore.YELLOW + 'WARNING', end='')
        print('] ' + message)
        with open('logs.txt', 'a+') as f:
            f.write('[WARNING@{}]: \n {} \n\n'.format(time(), message))
    if code == 2:
        print('[', end='')
        print(Fore.RED + 'ERROR', end='')
        print('] ' + message)
        with open('logs.txt', 'a+') as f:
            f.write('[ERROR@{}]: \n {} \n\n'.format(time(), message))
    if code == 3:
        if PRINT_DEBUG:
            print(Fore.WHITE + Back.BLUE +
                  '\b[DEBUG] {}'.format(message))
        with open('logs.txt', 'a+') as f:
            f.write('[DEBUG@{}]: \n {} \n\n'.format(time(), message))


def get_info(self, url):
    """return header and redirected url"""
    from requests import get
    from requests.packages.urllib3 import disable_warnings
    from requests.exceptions import ConnectionError, MissingSchema
    try:
        toast(0, 'Waiting for File INFO')
        dummy_request = get(
            url, headers={'Range': 'bytes=0-100',
                          'User-Agent': 'Mozilla/5.0(X11; Linux x86_64)'},
            stream=True)
        dummy_request.close()
        toast(0, 'Recived File INFO')
        # contains all the info
        recived_headers = dummy_request.headers
        final_url = dummy_request.url  # return the final url after redirecting
        return final_url, recived_headers

    except ConnectionError as e:
        try:
            disable_warnings()
            dummy_request = get(url, verify=False, stream=True, headers={'Range': 'bytes=0-100',
                                                                         'User-Agent': 'Mozilla/5.0(X11; Linux x86_64)'})
            self.verify = False
            dummy_request.close()
            toast(2, 'This url may contains Virus  as it\'s INSECURE')
            return dummy_request.url, dummy_request.headers
            toast(1, '{} May contains VIRUS'.format(url))
        except Exception:
            toast(2, 'get_headers: {}'.format(e))
        return url, {}
    except MissingSchema as e:
        toast(1, 'Do you mean http://{}/?'.format(url))
        return get_info(self, 'http://{}/'.format(url))
    except Exception as e:
        toast(2, 'get_info: {}'.format(e))
        return url, {}


def _is_downloadable(headers):
    """Return True/False if a link contains a file"""
    try:
        if 'html' not in headers['Content-Type']:
            return True
        else:
            return False
    except KeyError:
        return False

    except Exception as e:
        toast(2, '_is_downloadable: {}'.format(e))


def get_filename(url, headers, given_url):
    """Get file name from url and headers """
    try:
        from urllib.parse import unquote
        from time import time
        from cgi import parse_header
        url = unquote(url)
        if 'Content-Disposition' in headers:
            _param = parse_header(headers['Content-Disposition'])[1]
            if 'filename' in _param:
                filename = _param['filename']
                filename = filename.replace(":", " ").replace(
                    "/", "_").replace("\\", "_").replace("*", " ")
                filename = filename.replace(">", " ").replace(
                    "<", " ").replace("?", " ").replace("|", "_")
                return filename
            elif 'filename*' in _param:
                filename = _param['filename*']
                filename = filename.replace(":", " ").replace(
                    "/", "_").replace("\\", "_").replace("*", " ")
                filename = filename.replace(">", " ").replace(
                    "<", " ").replace("?", " ").replace("|", "_")
                return filename
            else:
                print(_param)
        else:
            filename = unquote(
                url.split('/')[-1]).replace('!', '').replace('?', '')
            filename = filename.replace(":", " ").replace(
                "/", "_").replace("\\", "_").replace("*", " ")
            filename = filename.replace(">", " ").replace(
                "<", " ").replace("?", " ").replace("|", "_")
            return filename
    except Exception as e:
        toast(2, 'get_filename: {}'.format(e))
        return 'File donwloaded @ {}'.format(int(time()))


def _is_pauseable(headers):
    """return bool for paauseable ?"""
    try:
        if headers['Content-Length'] == '101':
            return True
    except Exception as e:
        toast(2, '_is_pauseable: {}'.format(e))
    return False


def get_size(self):
    """ return file size """
    url, headers = self.url, self.recived_headers
    from requests import get
    try:
        return int(headers['Content-Range'].split('/')[-1])
    except KeyError as e:
        temp_requests = get(url, stream=True, verify=self.verify)
        temp_requests.close()
        return int(temp_requests.headers['Content-Length'])
    except Exception as e:
        toast(2, 'get_size: {}'.format(e))
    return -1


def p_unit(self):
    """ convert units and return string"""
    try:
        unit_list = ["B", "KB", "MB", "GB", "TB"]
        for unit in unit_list:
            magnitude = round(self / (1024 ** unit_list.index(unit)), 3)
            if magnitude > 0 and magnitude < 1000:
                return "{} {}".format(magnitude, unit)
    except Exception as e:
        toast(2, 'p_unit: {}'.format(e))
