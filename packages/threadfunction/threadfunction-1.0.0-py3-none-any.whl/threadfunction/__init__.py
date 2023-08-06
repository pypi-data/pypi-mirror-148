from threading import Thread, Lock, enumerate as thread_enumerate
from queue import Queue
import time
import uuid


class ThreadFunction:
    func_obj = None
    arg_list = None
    thread_function_args = None
    thread_obj = None
    args = None
    kwargs = None

    def __init__(self, this_function):
        self.func_obj = this_function
        self.func_name = this_function.__name__
        self.arg_list = this_function.__code__.co_varnames
        if 'thread_function_args' not in self.arg_list:
            raise RuntimeError('使用ThreadFunction装饰的函数必须添加名为thread_function_args的参数')
        super(ThreadFunction, self).__init__()

    def __call__(self, *args, **kwargs):
        return self.func_obj(*args, **kwargs)

    def __prepare__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.kwargs['__func_obj'] = self.func_obj
        if 'thread_function_args' in self.kwargs:
            self.thread_function_args = self.kwargs['thread_function_args']
        else:
            self.thread_function_args = ThreadFunctionArgs()
            self.kwargs['thread_function_args'] = self.thread_function_args

        if self.thread_function_args.task_uuid is None:
            self.thread_function_args.task_uuid = uuid.uuid4()
        if self.thread_function_args.task_name is None:
            self.thread_function_args.task_name = '{}_{}'.format(self.func_name, self.thread_function_args.task_uuid)
        self.thread_function_args.task_time = time.time()
        if self.thread_function_args.task_conc:
            if not isinstance(self.thread_function_args.task_conc, Concurrent):
                raise RuntimeError('thread_function_args.task_conc must be class <Concurrent>, got {}'.format(type(self.thread_function_args.task_conc)))
            self.thread_function_args.task_conc.wait()
        print('ThreadFunction ++++ {} {} {}'.format(
            self.thread_function_args.task_uuid, self.func_name, self.thread_function_args.task_name))

    def thread(self, *args, **kwargs):
        self.__prepare__(*args, **kwargs)
        task_name = self.thread_function_args.task_name
        task_uuid = self.thread_function_args.task_uuid
        self.thread_obj = Thread(target=run_function_by_thread, args=self.args, kwargs=self.kwargs)
        self.thread_obj.setName('{}_{}'.format(self.func_name, task_uuid))
        self.thread_obj.start()
        handler = ThreadFunctionHandler(func_name=self.func_name, task_uuid=task_uuid, task_name=task_name, thread_obj=self.thread_obj)
        return handler

    def wait(self, *args, **kwargs):
        handler = self.thread(*args, **kwargs)
        wait_threads(handler_list=[handler])
        return handler


class ThreadFunctionArgs:

    def __init__(self, task_name=None, task_uuid=None, task_time=None, task_lock=None, task_conc=None):
        self.task_name = task_name
        self.task_uuid = task_uuid
        self.task_time = task_time
        self.task_lock = task_lock
        self.task_conc = task_conc


class ThreadFunctionHandler:

    def __init__(self, func_name, task_uuid, task_name, thread_obj):
        self.func_name = func_name
        self.task_uuid = task_uuid
        self.task_name = task_name
        self.thread_obj = thread_obj
        self.running = True

    def __str__(self):
        return '{} {} {}'.format(self.func_name, self.task_name, self.task_uuid)

    def done(self):
        if self.thread_obj and not self.thread_obj.is_alive():
            print('ThreadFunction Done: {} {} {}'.format(self.task_uuid, self.func_name, self.task_name))
            self.running = False
            return True
        else:
            return False


class Concurrent:

    def __init__(self, size=None):
        if not isinstance(size, int):
            raise RuntimeError('need int type, got: {}'.format(type(size)))
        if size <= 0:
            raise RuntimeError('Concurrent size must > 0, got {}'.format(size))
        self.size = size
        self.queue = Queue(maxsize=size)
        print('Concurrent size: {}'.format(size))

    def wait(self):
        self.queue.put(1)

    def done(self):
        self.queue.get()


def run_function_by_thread(*args, **kwargs):
    __func_obj = kwargs.pop('__func_obj')
    __func_obj(*args, **kwargs)
    thread_function_args = kwargs['thread_function_args']
    if thread_function_args:
        if thread_function_args.task_conc:
            thread_function_args.task_conc.done()
            print('ThreadFunction ---- {}'.format(thread_function_args.task_uuid))

def get_thread_list():
    thread_list = []
    for threading_one in thread_enumerate():
        thread_list.append(threading_one.name)
    print('线程数：{}，线程清单：{}'.format(len(thread_list), ', '.join(thread_list)))
    return thread_list

def wait_threads(handler_list):
    while True:
        for handler in handler_list:
            if handler.running and not handler.done():
                break
        else:
            break
    get_thread_list()


def get_lock():
    return Lock()