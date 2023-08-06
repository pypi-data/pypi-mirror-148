## ThreadFunction

基于threading的多线程装饰器

#### 安装

```shell
pip3 install threadfunction
```

#### 示例
```python
from threadfunction import ThreadFunction,ThreadFunctionArgs,Concurrent,get_thread_list,wait_threads
import time

@ThreadFunction   #给任务函数添加装饰器,添加thread_function_args参数
def io_task(seconds, thread_function_args=None):
    time.sleep(seconds)
    return '执行完毕'

def test_threadfunction():
    handler_list = []
    # task_lock = get_lock()
    # task_lock = None
    task_conc = Concurrent(size=4)    #设置并发数
    for i in range(8):
        thread_function_args = ThreadFunctionArgs(task_conc=task_conc)
        handler = io_task.thread(seconds=1, thread_function_args=thread_function_args)    #启动线程
        handler_list.append(handler)
    
    get_thread_list()
    wait_threads(handler_list=handler_list)
    print('test_threadfunction pass')

if __name__ == '__main__':
    start = time.time()
    test_threadfunction()
    print(f'cost: {time.time() - start}s')

```