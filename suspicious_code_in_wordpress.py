import os
import sys
import shutil
import datetime
import time
import pyprind

pattern_suspicious_code = ['eval(base64_decode(', 'some text']


def count_time(func):
    def wrapped():
        str_time = time.time()
        obj = func()
        print('Lead time:', time.time() - str_time)
        return obj

    return wrapped


@count_time
def main():
    found_files = search_files()
    result = search_suspicious_code(found_files)
    write_stat_in_file(result)


def search_files():
    files_for_check = list()
    base_path = search_path()
    type_of_files = ext_files()
    for (dir_path, dir_names, file_names) in os.walk(base_path):
        for file in file_names:
            if type_of_files == '.html и .php':
                if file.endswith('html') or file.endswith('php'):
                    files_for_check.append(os.path.join(dir_path, file))
            else:
                if file.endswith(type_of_files):
                    files_for_check.append(os.path.join(dir_path, file))
    return files_for_check, base_path


def search_path():
    default_path_nt = ['D:\\jetbrains\\tmp']
    default_path_nix = ['/var/www/']
    if os.name == 'nt':
        sp = input(f'Where are we looking?\nexample: {default_path_nt[0]}\nOr press "Enter" '
                   f'to select the default path {default_path_nt[0]}\n')
        if os.path.isdir(sp):
            return sp
        elif len(sp) <= 0:
            return default_path_nt[0]
        else:
            print('This directory does not exist!')
            sys.exit()
    else:
        sp = input(f'Where are we looking?\nexample: /var/www/\nOr press "Enter" '
                   f'to select the default path {default_path_nix[0]}\n')
        if os.path.isdir(sp):
            return sp
        elif len(sp) <= 0:
            return default_path_nix[0]
        else:
            print('This directory does not exist!')
            sys.exit()


def ext_files():
    ext_input = {'1': '.html', '2': '.php', '3': '.html и .php'}
    exf = input('What files are looking for?\n 1 - .html\n 2 - .php\n 3 - .html и .php\n')
    exf = ext_input.get(exf)
    if exf is None:
        print('Wrong number menu item (:')
        sys.exit()
    else:
        return exf


def search_suspicious_code(value):
    stats_info = [f'In the directory {value[1]} found {len(value[0])} files to check.\n']
    bar = pyprind.ProgBar(len(value[0]), stream=sys.stdout)
    for path in value[0]:
        with open(path, encoding='utf8', mode='r+', errors='ignore') as fr:
            str_in_files = fr.readlines()
            line_count = 0
            suspicious_code = 0
            backup_count = 0
            suspicious_code_line = []
            for index, string in enumerate(str_in_files):
                line_count += 1
                for i in pattern_suspicious_code:
                    if i in string:
                        if backup_count == 0:
                            backup_done = (backup_file(path, value[1]))
                            backup_count += 1
                        if path.endswith('php'):
                            str_in_files[index] = '/*!!!-----------!!! Suspicious code was here !!!-----------!!!*/\n'
                            suspicious_code_line.append(line_count)
                        else:
                            str_in_files[
                                index] = '<!-- !!!-----------!!! Suspicious code was here !!!-----------!!! -->\n'
                            suspicious_code_line.append(line_count)
                        suspicious_code += 1
            if suspicious_code != 0:
                fr.seek(0)
                fr.truncate(0)
                for i in str_in_files:
                    fr.write(i)
                stats_info.append((
                    f'{suspicious_code} number of deleted lines in file {path}\nLine numbers where the code was deleted {suspicious_code_line}\n{backup_done}\n'))
                suspicious_code = 0
                backup_count = 0
            else:
                stats_info.append(f'Suspicious code in file {path} was not found!\n')
        bar.update()
    return stats_info, value[1]


def backup_file(path, base_path):
    destination = path + '_backup_file_' + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
    shutil.copy(path, destination)
    return f'Modified file saved as {destination}'


def write_stat_in_file(stat):
    if os.name != 'nt':
        path = f'{stat[1]}stat_{datetime.datetime.now().strftime("%Y_%m_%d_%H-%M-%S")}.txt'
        with open(path, 'w') as f:
            for i in stat[0]:
                f.write(i + '\n')
        print(f'Report Created {path}')
    else:
        path = f'{stat[1]}\\stat_{datetime.datetime.now().strftime("%Y_%m_%d_%H-%M-%S")}.txt'
        with open(path, 'w') as f:
            for i in stat[0]:
                f.write(i + '\n')
        print(f'Report Created {path}')


if __name__ == "__main__":
    main()
