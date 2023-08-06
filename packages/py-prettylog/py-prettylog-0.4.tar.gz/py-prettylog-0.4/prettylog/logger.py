import ntpath
import os
import datetime
from inspect import getframeinfo, stack
from typing import Tuple, Callable
from dataclasses import dataclass
from termcolor import colored
from queue import Queue
from pathlib import Path
from colorama import init

init()


def stack_info() -> Tuple[str, int]:
    caller = getframeinfo(stack()[3][0])
    return ntpath.basename(caller.filename), caller.lineno


LEVELS = {
    "debug": ["magenta"],
    "info": ["cyan"],
    "success": ["green"],
    "warning": ["yellow"],
    "error": ["red"],
    "critical": ["white", "on_red"]
}


@dataclass
class Callbacks:

    """
    This class creates a mapping of callback functions.
    Before every log function call returns, it will call the callback mapped to that logging level.
    
    Here's what every callback function should look like.

    >>> def on_debug(metadata: dict) -> None:
            '''
            Here's what the metadata looks like. Taken directly from `log()` source.
            {
                "level": level,
                "iso_date": dt.isoformat(),
                "file": fname,
                "file:lineno": f"{fname}:{no}",
                "text": text,
                "group": group
            }
            '''
    """

    on_debug: Callable = None
    on_info: Callable = None
    on_success: Callable = None
    on_warning: Callable = None
    on_error: Callable = None
    on_critical: Callable = None


class Logger:
    """
    Initialize the Logger.

    Levels
    ------
    The following are the levels and also the method names for each level.

    - debug
    - info
    - success
    - warning
    - error
    - critical


    Parameters
    ----------
    `folder` : str
        Where to store all the log files.
    `file_format` : str
        Format of each log file. Defaults to .log (. should be included)
    `format` : str
        Format of the logs. (This is not the same as file_format) Defaults to '[{file:lineno}] {text} {COLORED}'
    `debug` : bool  
        Debug mode. Defaults to False. If True, print_level and file_level will automatically be set to debug.
    `print_level` : str
        What level to print on. Anything above and at this level will be printed. Defaults to info.
    `file_level` : str
        What level to write on. Anything above and at this level will be written to a file. Defaults to warning.
    `encoding` : str
        Encoding to use when logging onto a file. Defaults to "utf-8"
    `separator` : str
        What separator to use when logging onto a file. Defaults to "\n"
    `cache_size` : int
        How many logs to store in the cache before updating the file again. Defaults to 5.
    `disabled_group_prints` : List[str]
        List of groups that are disabled for printing. Defaults to None
    `disabled_group_files` : List[str]
        List of groups that are disabled for writing to a file. Defaults to None
    `callbacks` : Callbacks
        A `Callbacks` class that contains callback functions to be called after each log coressponding that category.
    """

    def __init__(self, folder: str = None, **kwargs) -> None:
        self.folder = folder

        # Kwargs
        self.file_format = kwargs.get("file_format", ".log")
        self.format = kwargs.get("format", "[{file:lineno}] {text} {COLORED}")
        self._debug = kwargs.get("debug", False)
        self.print_level = kwargs.get("print_level", "info")
        self.file_level = kwargs.get("file_level", "warning")
        self.encoding = kwargs.get("encoding", "utf-8")
        self.separator = kwargs.get("separator", "\n")
        self.cache_size = kwargs.get("cache_size", 5)
        self.disabled_group_prints = kwargs.get("disabled_group_prints", [])
        self.disabled_group_files = kwargs.get("disabled_group_files", [])
        self.callbacks = kwargs.get("callbacks", Callbacks())

        # Create folder if it doesn't exist
        if folder:
            Path(folder).mkdir(exist_ok=True)

        if self._debug:
            self.print_level = "debug"
            self.file_level = "debug"

        self.cache = Queue()
        self.Cr1TiKal = self.critical

        self.default_group = "__main__"

    def get_log_files(self) -> dict:
        if self.folder is None:
            return {}

        files = {}
        for k in LEVELS.keys():
            files[k] = os.path.join(self.folder, f"{k}{self.file_format}")
        return files

    def _get_log_index(self, level: str) -> int:
        try:
            return list(LEVELS.keys()).index(level)
        except IndexError:
            return -1

    def format_log(self, log: dict, to_file: bool = False) -> str:
        format_string = self.format

        # Figure out whether to use colored output or not
        use_color = format_string.endswith(" {COLORED}")
        format_string = format_string.replace(" {COLORED}", "")
        if to_file:
            use_color = False

        for k, v in log.items():
            if k == "level":
                v = v.upper()
            format_string = format_string.replace("{" + k + "}", v)

        if use_color:
            format_string = colored(
                format_string, *LEVELS[log["level"]])
        return format_string
    
    def set_group(self, group: str) -> None:
        self.default_group = group

    def clear_cache(self) -> None:
        """Clears the cache and saves all the items in the cache in the log files."""

        with self.cache.mutex:
            logs = list(self.cache.queue)
            self.cache.queue.clear()

            if self.folder:
                output = {}

                file_level = self._get_log_index(self.file_level)
                for log in logs:
                    level = self._get_log_index(log["level"])

                    if not level < file_level:
                        if log["group"] not in self.disabled_group_files:
                            formatted = self.format_log(log, to_file=True)

                            if log["level"] not in output.keys():
                                output[log["level"]] = []
                            output[log["level"]].append(formatted)

                files = self.get_log_files()

                for level, logs in output.items():
                    fname = files.get(level)

                    if fname:
                        logs_joined = self.separator.join(logs)

                        with open(fname, "a", encoding=self.encoding) as f:
                            f.write(f"{logs_joined}{self.separator}")

    def _check_cache_size(self) -> None:
        if self.cache.qsize() >= self.cache_size:
            self.clear_cache()

    def debug(self, text: str, **kwargs) -> str:
        return self.log(text, "debug", **kwargs)

    def info(self, text: str, **kwargs) -> str:
        return self.log(text, "info", **kwargs)

    def success(self, text: str, **kwargs) -> str:
        return self.log(text, "success", **kwargs)

    def warning(self, text: str, **kwargs) -> str:
        return self.log(text, "warning", **kwargs)

    def error(self, text: str, **kwargs) -> str:
        return self.log(text, "error", **kwargs)

    def critical(self, text: str, **kwargs) -> str:
        return self.log(text, "critical", **kwargs)

    def log(self, text: str, level: str = "info", **kwargs) -> str:
        """
        Log. You should use the other methods rather than this.

        Parameters
        ----------
        `text` : str
            What to log.
        `level` : str
            What level the log should be.
        `group` : str
            What group this current log belongs to. Defaults to self.default group which is __main__ by default but it can be modified using the set_group method.
        `**kwargs` :
            Other kwargs will be passed onto the callback function if it exists.

        Returns
        -------
        The log itself but formatted.
        """

        # Get stack info (File name, Line no.)
        fname, no = stack_info()
        group = kwargs.pop("group", self.default_group)

        # Construct metadata
        dt = datetime.datetime.now()
        metadata = {
            "level": level,
            "iso_date": dt.isoformat(),
            "file": fname,
            "file:lineno": f"{fname}:{no}",
            "text": text,
            "group": group
        }

        print_level = self._get_log_index(self.print_level)
        current_level = self._get_log_index(level)
        formatted = self.format_log(metadata)

        if not current_level < print_level:
            if group not in self.disabled_group_prints:
                print(formatted)

        # Put in the cache for file use later on.
        self.cache.put(metadata)

        # Check if we have to dump the cache
        self._check_cache_size()

        # Call the callback function related to this log if it exists.
        try:
            callback_function = getattr(self.callbacks, f"on_{level}")
        except AttributeError:
            callback_function = None
        
        if callback_function is not None:
            callback_function(metadata, **kwargs)

        return formatted
