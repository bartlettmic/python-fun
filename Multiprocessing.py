from multiprocessing import Process, cpu_count
import os

_global = "Dicks"

def info(title):
    print(title)
    print(_global)
    print('module name:', __name__)
    if hasattr(os, 'getppid'):  # only available on Unix
        print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print('-'*10)

if __name__ == '__main__':
    info('main line')
    p = Process(target=info, args=('child',))
    p.start()
    p.join()
    print(cpu_count())