import os
import platform


def search(a):
    file_name_list = []
    sep = '\\'
    if platform.system() == 'Linux':
        sep = '/'
    for file in os.listdir(a):
        if os.path.isfile(a + sep + file):
            print(file, '=>', a + sep + file)
        else:
            file_name_list.append(file)

    return file_name_list


if __name__ == "__main__":
    # directories = search(os.path.abspath('./static'))
    # print(directories)
    arr = ['a', 'b']
    str1 = ','.join(arr)
    print(str1)


