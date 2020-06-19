import platform

from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko
import os

allowed_command = ['ps', 'tail', 'python']


def hello(request):
    tail_text = os.popen(r'tail -n 10 /home/cyanks/github/pySpider/lianjia/lianjia.log').read()
    array = tail_text.split('\n')
    return HttpResponse('<br>'.join(array))


def new_hello(request):
    return render(request, 'hello.html')


def gallery(request):
    param = [1, 2, 15, 62, 9, 43]
    return render(request, 'gallery.html', locals())


def get_album_list(request):
    a_dir = os.path.abspath('./static')
    file_name_list = []
    sep = '\\'
    if platform.system() == 'Linux':
        sep = '/'
    for file in os.listdir(a_dir):
        if os.path.isfile(a_dir + sep + file):
            print(file, '=>', a_dir + sep + file)
        else:
            file_name_list.append(file)

    return HttpResponse(','.join(file_name_list))


def get_file_list(request):
    req_dir = request.GET.get('dir')
    file_name_list = []
    a_dir = os.path.abspath('./static/%s' % req_dir)
    sep = '\\'
    if platform.system() == 'Linux':
        sep = '/'
    for file in os.listdir(a_dir):
        if os.path.isfile(a_dir + sep + file):
            file_name_list.append('/static/%s/%s' % (req_dir, file))
        else:
            print('It\'s a dir')
    return render(request, 'gallery.html', locals())


def exec_command(comm):
    hostname = '10.11.12.33'
    username = 'cyanks'
    password = 'asdf'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(comm)
    result = stdout.read()
    ssh.close()
    return result


@accept_websocket
def echo_once(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            checked = check_command(message)
            print('Received message: %s' % message)
            if checked:  # 这里根据web页面获取的值进行对应的操作
                command = 'tail -n 100 /home/cyanks/github/pySpider/lianjia/lianjia.log'#''tail -n 100 /home/cyanks/github/pySpider/lianjia/lianjia.log'  # 这里是要执行的命令或者脚本

                # 远程连接服务器
                hostname = '10.11.12.33'
                username = 'cyanks'
                password = 'asdf'

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname, username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                steps = 0
                while steps<1000:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    # print(nextline.strip())
                    # 判断消息为空时,退出循环
                    if not nextline:
                        print('未获取到内容')
                    else:
                        request.websocket.send(nextline)  # 发送消息到客户端

                ssh.close()  # 关闭ssh连接
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))


def check_command(message):
    for allowed in allowed_command:
        if allowed in message:
            return True
    return False
