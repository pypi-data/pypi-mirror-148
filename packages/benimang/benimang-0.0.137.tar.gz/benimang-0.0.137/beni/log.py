import logging
import re
from pathlib import Path
from typing import Any, Callable, Final, Sequence, TextIO, Tuple, TypeVar

import colorama
from colorama import Fore
from prettytable import PrettyTable

import beni
import beni.print as bprint

_loggerName = 'beni'

_countWarning: int = 0
_countError: int = 0
_countCritical: int = 0


def init(loggerName: str = '', loggerLevel: int = logging.INFO, logFile: Path | None = None):
    LOGGER_FORMAT = '%(asctime)s %(levelname)-1s %(message)s', '%Y-%m-%d %H:%M:%S'
    LOGGER_LEVEL_NAME = {
        logging.DEBUG: 'D',
        logging.INFO: '',
        logging.WARNING: 'W',
        logging.ERROR: 'E',
        logging.CRITICAL: 'C',
    }

    if loggerName:
        global _loggerName
        _loggerName = loggerName

    logger = logging.getLogger(_loggerName)
    logger.setLevel(loggerLevel)
    for loggingLevel, value in LOGGER_LEVEL_NAME.items():
        logging.addLevelName(loggingLevel, value)

    loggerFormatter = logging.Formatter(*LOGGER_FORMAT)

    class CustomStreamHandler(logging.StreamHandler):

        stream: TextIO

        def emit(self, record: logging.LogRecord):
            try:
                msg = self.format(record) + self.terminator
                # issue 35046: merged two stream.writes into one.
                func = self.stream.write
                if record.levelno == logging.WARNING:
                    global _countWarning
                    _countWarning += 1
                    bprint.set_color(Fore.YELLOW)

                elif record.levelno == logging.ERROR:
                    global _countError
                    _countError += 1
                    bprint.set_color(Fore.LIGHTRED_EX)
                elif record.levelno == logging.CRITICAL:
                    global _countCritical
                    _countCritical += 1
                    bprint.set_color(Fore.LIGHTMAGENTA_EX)
                func(msg)
                bprint.clear_color()
                self.flush()
            except RecursionError:  # See issue 36272
                raise
            except Exception:
                self.handleError(record)

    loggerHandler = CustomStreamHandler()
    loggerHandler.setFormatter(loggerFormatter)
    loggerHandler.setLevel(loggerLevel)
    logger.addHandler(loggerHandler)

    if logFile:

        class CustomFileHandler(logging.FileHandler):

            _write_func: Any
            _xx = re.compile(r'\x1b\[\d+m')

            def _open(self):
                result = super()._open()
                self._write_func = result.write
                setattr(result, 'write', self._write)
                return result

            def _write(self, msg: str):
                msg = self._xx.sub('', msg)
                self._write_func(msg)

        beni.makedir(logFile.parent)
        fileLoggerHandler = CustomFileHandler(logFile, delay=True)
        fileLoggerHandler.setFormatter(loggerFormatter)
        fileLoggerHandler.setLevel(loggerLevel)
        logger.addHandler(fileLoggerHandler)


def debug(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).debug(msg, *args, **kwargs)


def info(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).info(msg, *args, **kwargs)


def warning(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).warning(msg, *args, **kwargs)


def error(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).error(msg, *args, **kwargs)


def critical(msg: Any, *args: Any, **kwargs: Any):
    logging.getLogger(_loggerName).critical(msg, *args, **kwargs)


def getcount_warning():
    return _countWarning


def setcount_warning(value: int):
    global _countWarning
    _countWarning = value


def getcount_error():
    return _countError


def setcount_error(value: int):
    global _countError
    _countError = value


def getcount_critical():
    return _countCritical


def setcount_critical(value: int):
    global _countCritical
    _countCritical = value


_T = TypeVar('_T')


def table(
    data_list: Sequence[_T],
    *,
    title: str | None = None,
    fields: Sequence[Tuple[str, Callable[[_T], Any]]],
    rowcolor: Callable[[list[Any]], Any] | None = None,
    extend: list[list[Any]] | None = None,
):
    header_color: Final = colorama.Fore.YELLOW
    table = PrettyTable()
    if title:
        table.title = bprint.get_str(title, header_color)
    field_funclist: list[Callable[[_T], Any]] = []
    field_namelist: list[str] = []
    align_dict: dict[str, str] = {}
    for i in range(len(fields)):
        item = fields[i]
        field_funclist.append(item[1])
        field_name = item[0]
        if field_name.endswith('>'):
            field_name = field_name[:-1]
            align_dict[field_name] = 'r'
        elif field_name.endswith('<'):
            field_name = field_name[:-1]
            align_dict[field_name] = 'l'
        field_namelist.append(field_name)
    table.field_names = [bprint.get_str(x, header_color) for x in field_namelist]
    for k, v in align_dict.items():
        table.align[bprint.get_str(k, header_color)] = v
    row_list: list[list[Any]] = []
    for data in data_list:
        row = [func(data) for func in field_funclist]
        row_list.append(row)
    if extend:
        row_list.extend(extend)
    if rowcolor:
        for row in row_list:
            color = rowcolor(row)
            if color:
                for i in range(len(row)):
                    row[i] = bprint.get_str(row[i], color)
    table.add_rows(row_list)
    info('\n'.join([
        '', '',
        table.get_string(),
        '',
    ]))
