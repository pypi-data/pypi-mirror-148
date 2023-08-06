import time
import gevent
import gevent.pool
from gevent.timeout import Timeout
# thread=True，会阻止主线程执行
from gevent import monkey; monkey.patch_all(thread=False)
from functools import partial
from collections import Iterable

from .utils import get_timeout
from .error_class import AsyncUtilError


class AsyncUtil:

    def __init__(self, targets: Iterable, max_async: int = None, response_type: str = 'null',
                 tries: int = 3, delay: float = 0):
        assert (max_async is None or 1 < max_async <= 1000), 'param <max_async> please enter in 2-1000 number value'
        assert response_type in ('null', 'obj', 'list', 'dict', 'struct'), 'param <response_type> enter error'
        self.max_async = max_async
        self.response_type = response_type
        self.targets = self.parse_targets(targets)
        self.response = self._init_type()
        self.tries, self.delay = tries, delay
        self.async_pool = gevent.pool.Pool(len(self.targets))

    def _init_type(self):
        """ init result data type """
        if self.response_type in ('obj', 'list', 'struct'):
            return []
        elif self.response_type == 'dict':
            return {}
        elif self.response_type == 'null':
            return None

    def parse_targets(self, targets):
        """ parse task list, for async_utils exec """
        parse_result = []

        # append exec target to list
        def _loops(way):
            for _iter in targets:
                func, args, kwargs = _iter.get('target'), _iter.get('args', ()), _iter.get('kwargs', {})
                if not (hasattr(func, '__call__') and isinstance(args, tuple) and isinstance(kwargs, dict)):
                    raise AsyncUtilError('param <targets> format enter error')
                parse_result.append(partial(way, partial(func, *args, **kwargs)))

        # for save diff response
        def _o(f): self.response.append(f())
        def _l(f): self.response += f()
        def _d(f): self.response.update(f())
        def _s(f): self.response.append({f.func.__name__: f()})
        def _n(f): f()
        mapping = {'obj': _o, 'list': _l, 'dict': _d, 'struct': _s, 'null': _n}
        _loops(mapping[self.response_type])
        return parse_result

    def all_load(self):
        workspace = [self.async_pool.spawn(func) for func in self.targets]
        gevent.joinall(workspace)

    def batch_load(self):
        while self.targets:
            queue = self.targets[:self.max_async]
            if not queue:
                continue
            workspace = [self.async_pool.spawn(func) for func in queue]
            gevent.joinall(workspace)
            time.sleep(self.delay)
            self.targets = self.targets[self.max_async:]

    def _monitor(self, load_obj, tries, delay):
        """monitor manage load obj (timeout or error or retry)"""

        def __handle(_tries):
            _tries -= 1
            if _tries <= 0:
                raise
            time.sleep(delay)
            if self.max_async is None:      # result clean(data not repeat)
                self.response = self._init_type()
            self._monitor(load_obj, _tries, delay)      # retry

        timeout = Timeout(get_timeout(len(self.targets)))
        timeout.start()
        try:
            load_obj()
        except Timeout:
            __handle(tries)
        except:
            __handle(tries)
        finally:
            timeout.cancel()

    def working(self):
        """ for run task list """
        if self.max_async is None:
            self._monitor(self.all_load, self.tries, self.delay)
        else:
            self._monitor(self.batch_load, self.tries, self.delay)
        self.clean()
        return self.response

    def clean(self):
        """clean up unused memory"""
        del (self.targets, self.max_async, self.response_type, self.tries, self.delay, self.async_pool)

