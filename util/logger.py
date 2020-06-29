import json
import logging
import os
import socket
import sys
from collections import OrderedDict

from util import datetime_helper


class LoggerFormatter(logging.Formatter):
    """
    日志记录格式化
    """

    def format(self, record: logging.LogRecord):
        super().format(record)
        s = record.message
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text

        # 计算method_name
        cls_name = ''
        func_name = record.funcName
        count = 40
        f = sys._getframe()
        while f.f_code.co_name != func_name and count > 0:
            f = f.f_back
            count -= 1
        func_frame = f if f.f_code.co_name == func_name else None
        caller = func_frame.f_locals.get('self', None) if func_frame else None

        try:
            if caller:
                if not hasattr(caller, '__name__'):
                    caller = caller.__class__
                cls_name = '%s.%s' % (caller.__module__, caller.__name__)
        except:
            pass
        finally:
            method_name = '{cls_name}.{func_name}'.format(cls_name=cls_name, func_name=func_name)
        try:
            local_ip = socket.gethostbyname(socket.gethostname())  # 本地调试会报错
        except:
            local_ip = None
        msg = OrderedDict((
            ('@timestamp', datetime_helper.get_time_str()),
            ('level', record.levelname),
            ('project_name', os.environ.get('PROJECT_NAME', '')),
            ('project_version', os.environ.get('PROJECT_VERSION', '')),
            ("request_uri", getattr(record, 'request_uri', "")),
            ("trace_id", getattr(record, 'trace_id', "")),  # todo 通过thread获取trace_id?
            ("remote_ip", getattr(record, 'remote_ip', "")),
            ("user", getattr(record, 'user', "")),
            ("local_ip", local_ip),
            ("logger_name", record.name),
            ("method_name", method_name),
            ("line_number", record.lineno),
            ("thread_name", record.threadName),
            ("message", s),
            ("stack_trace", record.stack_info),
        ))
        return json.dumps(msg)
