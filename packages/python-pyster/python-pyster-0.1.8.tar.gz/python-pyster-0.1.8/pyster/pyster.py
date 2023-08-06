import inspect
import time
import options
from endreport import Endreport
from errors import non_overridable_error as nomo
from errors import test_failure
#import timeit
import types
import typing
import sys
import traceback
from rich import console, syntax, theme, text
import contextlib, io
import re


def is_printable(s):
    return not any(repr(ch).startswith("'\\x") or repr(ch).startswith("'\\u") for ch in s)

def ignore(func):
    ''' Wrapper used in classes to ignore functions'''
    func._ignore_for_pyster = True
    return func

class Style():
    CUSTOM_THEMES = theme.Theme({
        "debug": "bold dim cyan",
        "warning": "bold yellow",
        "err": "bold red",
        "success": "bold green",
        "info": "bold blue",
        "warning": "dim bold yellow",
        "running": "bold magenta"
    })

    DEFAULT_STYLE = {
        "status_bar": True,
        "print_doc": True,
        "measure_time": True,
        "running_message": "  [running]<TEST>[/running]     [bold]%s[bold]",
        "passed_message": "    [success][PASS][/success]   %s",
        "failed_message": "    [err][FAIL][/err]   %s",
        "failed_error_name": "    [err][ERROR][/err]  [bold cyan]%s[/bold cyan]",
        "failed_error_info": ":   %s",
        "debug_message": "    [debug][DEBUG][/debug]  %s",
        "info_message": "    [info][INFO][/info]   %s",
        "runtime_message": "    [info][INFO][/info]   The test ran in => [debug]%s[/debug] <="
        

    }
    
    # ! USE THE FILE=sys.stdout or the timer functions swallow everything
    ORIGIN_STDOUT = sys.stdout
    console = console.Console(theme=CUSTOM_THEMES, file=ORIGIN_STDOUT, color_system="standard") # ? Should I use this? theme=theme.Theme({"repr.number": "white on black"})
    status = console.status('', refresh_per_second=10, spinner="bouncingBar") # dots or bouncingBar
    status.start()
    def __init__(self, style_dict={}, **kwargs):
        self.style = {}
        self.style.update(self.DEFAULT_STYLE)
        
        #self.status.update(status="[bold green] ...", speed=0.5)
        
        # Either use the style_dict or kwargs! BUT not both
        if style_dict != {}:
            self.style.update(style_dict)
        elif kwargs != {}:
            self.style.update(kwargs)

    
    def get(self, field) -> object:
        return self.style.get(field)

    def print_runtime(self, time):
        time = round(time, 4)
        if float(time) > 1 and float(time) < 2:
            time = f"{time:.4f}sec"
        elif float(time) > 2:
            time = f"{time:.4f}secs"
        else:
            time = f"{time:.4f}ms"
        self.console.print(self.get("runtime_message")%time)

    def print_run(self, func):
        self.console.print(self.get("running_message")%(func.__module__.replace('.', '/')+"::"+func.__name__))

    def print_doc(self, str_):
        """ Print the __doc__ of the test. (In pyster its used for describing the task)"""
        self.console.print(self.get("info_message")%str_)
    
    def print_passed(self, func):
        self.console.print(self.get("passed_message")%func.__name__)

    def print_failed(self, func, err):
        self.console.print(self.get("failed_message")%func.__name__)
        info = repr(err).replace(str(type(err)).replace("<class '", "").replace("'>", ""), '').replace('()', '')
        if len(info) > 0:
            self.console.print((self.get("failed_error_name")+self.get("failed_error_info"))%(str(type(err)).replace("<class '", "").replace("'>", ""), info))
        else:
            self.console.print(self.get("failed_error_name")%str(type(err)).replace("<class '", "").replace("'>", ""))
        
        self.status.stop()
        con_ = console.Console(theme=self.CUSTOM_THEMES, color_system='standard') # TODO: Figure out this bug. Guess: probably sth with stdout

        for i, line in enumerate(traceback.format_exc().splitlines()[:-1]):
            s_ = syntax.Syntax(line, "python", theme="ansi_dark")
            if len(traceback.format_exc().splitlines()[:-1]) == i+1:
                con_.print('    [err][ERROR][/err]  [err]=>[/err]', end='')
                line = re.sub(r'^  ', '', line)
                s_ = syntax.Syntax(line, "python", theme="ansi_dark")
                
            else:
                con_.print('    [err][ERROR][/err]  ', end='')
            con_.print(line)
        con_ = None
        self.print_status(func)
        self.status.start()
        #self.console.print_exception(show_locals=True)
        
    def print_debug(self, debug):
        if len(debug) != 0:
            for line in debug.strip().split('\n'):
                self.console.print(self.get("debug_message")%line)
    
    def print_status(self, func):
        self.status.update(status=f"[dim bold] Testing[/dim bold] [cyan bold]{func.__name__}[/cyan bold]")



class NonOverridable(type):
    def __new__(self, name, bases, dct):
        if bases and "_run" in dct:
            raise nomo.NonOverridableError("Overriding _run is not allowed")
        return type.__new__(self, name, bases, dct)
class Test(metaclass=NonOverridable):
    def __init__(self) -> None:
        pass

    def _run(self, class_, style) -> None:
        methods = [x for x, y in class_.__dict__.items() if isinstance(y, (types.FunctionType))]
        #methods = [getattr(self, m) for m in dir(self) if not m.startswith('__') and not m.startswith("run")]
        for method_str in methods:
            if not method_str.startswith("__") and not method_str.endswith("__"):
                method = getattr(self, method_str)
                
                if not hasattr(method, "_ignore_for_pyster"):
                    #print(f"Calling method {method.__name__}()")
                    if Endreport.use:
                        Report(method, style=style, endreport=Endreport)
                    else:
                        Report(method, style=style)

class Report():
    def __init__(self, func, endreport=None, style=None) -> None:
        if style != None:
            self.style = style
        else:
            self.style = Style()
        self.endreport = endreport
        self.report(func)

    def report(self, func):
        self.style.print_status(func)
        self.style.print_run(func)
        try:
            if self.style.get("print_doc") and func.__doc__:
                self.style.print_doc(func.__doc__)
            
            if self.endreport:
                t, debug, err = timer(func)
                if err:
                    raise err
                self.style.print_debug(debug.getvalue())
                
                    
                self.endreport.add_time(func.__name__, t)
                if self.style.get("measure_time"):
                    self.style.print_runtime(t) # Execution time actually
                    
            else:
                if self.style.get("measure_time"):
                    t, debug, err = timer(func)
                    if err:
                        raise err
                    self.style.print_debug(debug.getvalue())
                    self.style.print_runtime(t) # Execution time actually
                else:
                    debug = io.StringIO() #! Be aware that this would also swallow every rich operation. The way to solve it is the following: set the file attr of the rich console to sys.stdout when its not yet used
                    with contextlib.redirect_stdout(debug):
                        func()
                    self.style.print_debug(debug.getvalue())
            if self.endreport:        
                self.endreport.add_status(func.__name__, True)
            self.style.print_passed(func)
        except Exception as err:
            if self.endreport:
                self.endreport.add_status(func.__name__, False)
            self.style.print_debug(debug.getvalue()) # Print debug messages even if there is an error
            self.style.print_failed(func, err)
            if not options.Options.no_error:
                if not options.Options.one_error:
                    raise test_failure.TestFailure(f'The function/method named {func.__name__} failed during testing!')



def run(style=None) -> None:
    if style != None:
        custom_style = style
    else:
        custom_style = Style()

    # The module from where the main is called from
    module = inspect.getmodule(inspect.stack()[1][0])
    all_classes = (obj for name, obj in inspect.getmembers(sys.modules[module.__name__], inspect.isclass)
          if obj.__module__ is module.__name__)
    for class_ in all_classes:
        for parent in class_.__mro__:
            if parent == Test:
                test_instance = class_()
                test_instance._run(class_, style=custom_style)




def wrapper(*args, **kwargs):
    if kwargs == {}:
        if Endreport.use:
            Report(args[0], endreport=Endreport, style=kwargs.get("style"))
        else:
            Report(args[0], style=kwargs.get("style"))
    def inner(func):
        if Endreport.use:
            Report(func, endreport=Endreport, style=kwargs.get("style"))
        else:
            Report(func, style=kwargs.get("style"))
    return inner
        
    
    

def timer(func):
    f = io.StringIO() #! Be aware that this would also swallow every rich operation. The way to solve it is the following: set the file attr of the rich console to sys.stdout when its not yet used
    with contextlib.redirect_stdout(f):
        start_ = time.time()
        try:
            func()
        except Exception as err:
            return None, f, err
        stop_ = time.time()
    return stop_-start_, f, None

