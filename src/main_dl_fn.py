def _download(self, _range, _id):
    from requests import get
    from req_fn import toast
    from os.path import getsize
    from os import remove
    try:
        if _range[0] != 0:
            first = _range[0] + 1
        else:
            first = _range[0]
        try:
            if self.pauseable:
                _already_done = getsize(self.location + self.file_name +
                                        '.' + str(_id) + '.odm')
                self.done += _already_done
                first += _already_done
            else:
                toast(1, 'Opps! Not Resumeable it\'s seems')
                remove(self.location + self.file_name +
                       '.' + str(_id) + '.odm')
        except FileNotFoundError as e:
            pass
        if first <= _range[1]:
            main_request = get(
                self.url, headers={
                    'Range': 'bytes={}-{}'.format(first, _range[1]),
                    'User-Agent': 'Mozilla/5.0(X11; Linux x86_64)'},
                stream=True, verify=self.verify)
            for data in main_request.iter_content(chunk_size=4096):
                with open(self.location + self.file_name +
                          '.' + str(_id) + '.odm', 'ab+') as file:
                    file.write(data)
                    if self.paused:
                        break
                with self.update_lock:
                    self.done += 4096
        self.no_completed += 1
    except Exception as e:
        toast(2, '_download: {}'.format(e))


def _writer(self):
    from req_fn import toast
    try:
        from os import remove
        from os.path import getsize
        if self.no_completed == self.no_of_parts:
            with open(self.location + self.file_name, 'wb') as file:
                for _ in range(self.no_of_parts):
                    with open(self.location + self.file_name + '.' +
                              str(_) + '.odm', 'rb') as p_file:
                        for data in p_file:
                            file.write(data)
        if getsize(self.location + self.file_name) == self.size:
            for _ in range(self.no_of_parts):
                remove(self.location + self.file_name + '.' +
                       str(_) + '.odm')
    except Exception as e:
        toast(2, '_writer: {}'.format(e))
