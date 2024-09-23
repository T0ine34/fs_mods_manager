from threading import Thread, Lock
from typing import Callable, Any
from enum import Enum

def chrono(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start} seconds")
        return result
    return wrapper

class Task:
    class STATE(Enum):
        PENDING = 0
        RUNNING = 1
        FINISHED = 2
    def __init__(self, func : Callable[[Any], Any], *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.__state = Task.STATE.PENDING
        self.__result = None
        
    def run(self):
        if self.__state != Task.STATE.PENDING:
            raise Exception("Task already running")
        self.__state = Task.STATE.RUNNING
        self.__result = self.__func(*self.__args, **self.__kwargs)
        self.__state = Task.STATE.FINISHED
        
    def __call__(self):
        self.run()
        
    def getState(self) -> 'Task.STATE':
        return self.__state
    
    def getResult(self) -> Any:
        if self.__state != Task.STATE.FINISHED:
            raise Exception("Task not finished")
        
        return self.__result
    
    def __str__(self):
        args = ", ".join([str(arg) for arg in self.__args]+[f"{key}={value}" for key, value in self.__kwargs.items()])
        return f"{self.__func.__name__}({args})"
    
    
    
class Runner:
    def __init__(self, onTaskFinished : Callable[[Task], Any] = None):
        self.__tasksToRun = [] #type: list[Task]
        self.__taskDone = [] #type: list[Task]
        self.__onTaskFinished = onTaskFinished
        self.__threads = [] #type: list[Thread]
        self.__running = False
        
    def addTask(self, task : Task):
        self.__tasksToRun.append(task)
            
    def __run(self, threadID : str = None):
        print(f"Thread {threadID} started")
        while self.__running and self.__tasksToRun:
            task = self.__tasksToRun.pop(0)
            task.run()
            self.__taskDone.append(task)
            if self.__onTaskFinished is not None:
                self.__onTaskFinished(task)
        
        if threadID is not None:
            print(f"Thread {threadID} finished")
        
    def runSync(self):
        self.__running = True
        self.__run()
                
    def runAsync(self, nbThreads = 1, wait = False):
        self.__running = True
        for i in range(nbThreads):
            thread = Thread(target=self.__run, args=(i,), name=f"Thread-{i}")
            thread.start()
            self.__threads.append(thread)
            
        if wait:
            for thread in self.__threads:
                thread.join()
        
            
    def getTasks(self) -> list[Task]:
        return self.__taskDone
    
    def stop(self):
        """force stop all threads"""
        self.__running = False
        print("Stopping all threads")
        for thread in self.__threads:
            print(f"Stopping thread {thread}")
            thread.join()
        
    

if __name__ == "__main__":
    from time import sleep
    import tkinter as tk
    from tkinter import ttk
    
    root = tk.Tk()
    root.title("Task runner")
    root.geometry("200x200")
    progress = ttk.Progressbar(root, mode="determinate", maximum=100)
    progress.pack(expand=True, fill="both")
    
    def testFunc(a : int, b : int) -> int:
        sleep(0.5)
        return a + b
    
    def onDone(task : Task):
        print(f"Task {task} finished and returned {task.getResult()}")
        progress.step(100/50)
        progress.update()
    
    @chrono
    def main():
        runner = Runner(onDone)
        
        tasks = [Task(testFunc, a, 2) for a in range(50)]
        for task in tasks:
            runner.addTask(task)
        runner.runAsync(1)
        
        def stop():
            runner.stop()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", lambda: stop())
        
    main()
    root.mainloop()