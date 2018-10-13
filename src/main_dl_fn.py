def _download(self, _range, _id):
    from requests import get
    from req_fn import toast
    from os.path import getsize
    from os import remove
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
                toast(1, 'Opps! Not Resumeable it\'s seems')
                remove(part_name)
        except FileNotFoundError:
            pass
        if _id == (self.no_of_parts - 1):
            if first < _range[1]:
                main_request = get(
                    self.url, headers={
                        'Range': 'bytes={}-{}'.format(first, _range[1]),
                        'User-Agent': 'Mozilla/5.0(X11; Linux x86_64)'},
                    stream=True, verify=self.verify)
                with open(part_name, 'ab+') as file:
                    for data in main_request.iter_content(chunk_size=4096):
                        written_bytes = file.write(data)
                        if self.paused:
                            break
                        with self.update_lock:
                            self.done += written_bytes
        else:
            if first < (_range[1] + 1):
                main_request = get(
                    self.url, headers={
                        'Range': 'bytes={}-{}'.format(first, _range[1]),
                        'User-Agent': 'Mozilla/5.0(X11; Linux x86_64)'},
                    stream=True, verify=self.verify)
                with open(part_name, 'ab+') as file:
                    for data in main_request.iter_content(chunk_size=4096):
                        written_bytes = file.write(data)
                        if self.paused:
                            break
                        with self.update_lock:
                            self.done += written_bytes
        self.no_completed += 1
    except Exception as e:
        toast(2, '_download[{}]: {}'.format(e.__traceback__.tb_lineno, e))


def _writer(self):
    if self.no_of_parts != 1:
        self._written = 0
        from req_fn import toast
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
            toast(2, '_writer[{}]: {}'.format(e.__traceback__.tb_lineno, e))
