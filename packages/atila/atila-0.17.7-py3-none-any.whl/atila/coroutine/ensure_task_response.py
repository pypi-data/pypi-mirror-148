from skitai.exceptions import HTTPError
from skitai.utility import make_pushables
import sys
from skitai.wastuff.api import API
import ctypes
from rs4.misc import producers
from rs4.protocols.sock.impl.ws import *
from skitai.tasks import proto
from . import utils
from skitai.tasks import tasks
from skitai.tasks.tasks import DEFAULT_TIMEOUT
from skitai.tasks.pth import sp_task
from skitai.tasks.pth import task as pth_task
from skitai.utility import deallocate_was
from skitai.backbone.threaded import trigger
from ..events import *

class ResponsibleTask:
    def _get_was (self):
        _was = utils.get_cloned_was (self.meta ['__was_id'])
        if "coro" in self.meta: # deciving `was` object
            utils.deceive_was (_was, self.meta ["coro"])
        return _was

    def _late_respond (self, tasks_or_content):
        if hasattr (self._was, 'websocket'):
            self._fulfilled (self._was, tasks_or_content)
            return

        # NEED self._fulfilled and self._was
        if not hasattr (self._was, 'response'):
            # already responsed: SEE app2.map_in_thread
            return

        response = self._was.response
        content = None
        expt  = None

        try:
            if self._fulfilled == 'self':
                content = tasks_or_content.fetch ()
            else:
                content = self._fulfilled (self._was, tasks_or_content)
            self._fulfilled = None

        except MemoryError:
            raise

        except HTTPError as e:
            response.start_response (e.status)
            content = content or response.build_error_template (e.explain or (self._was.app.debug and e.exc_info), e.errno, was = self._was)
            expt = sys.exc_info ()

        except:
            self._was.traceback ()
            response.start_response ("502 Bad Gateway")
            content = content or response.build_error_template (self._was.app.debug and sys.exc_info () or None, 0, was = self._was)
            expt = sys.exc_info ()

        if isinstance (content, API) and self._was.env.get ('ATILA_SET_SEPC'):
            content.set_spec (self._was.app)

        will_be_push = make_pushables (response, content)
        if will_be_push is None:
            return # future

        request_postprocessing (self._was, content, expt)


# request processing ------------------------------------------------
def request_postprocessing (was, content, exc_info = None):
    def respond (was, content, waking = False):
        if isinstance (content, producers.Sendable): # IMP: already sent producer
            return deallocate_was (was)

        will_be_push = make_pushables (was.response, content)
        if will_be_push is not None:
            for part in will_be_push:
                was.response.push (part)

        if waking:
            trigger.wakeup (lambda p = was.response, x = was: (p.done (), deallocate_was (x)))
        else:
            was.response.done ()
            deallocate_was (was)

    def postprocess (was, content, exc_info, depends, hooks):
        success, failed, teardown = hooks
        try:
            try:
                if exc_info is None:
                    for func in depends:
                        content = was.execute_function (func, (was,)) or content
                    if success:
                        content = was.execute_function (success, (was, content)) or content
                    was.app.emit (EVT_REQ_SUCCESS, content)
                else:
                    if failed:
                        content = was.execute_function (failed, (was, exc_info)) or content
                    was.app.emit (EVT_REQ_FAILED, exc_info)

            finally:
                teardown and was.execute_function (teardown, (was,))
                was.app.emit (EVT_REQ_TEARDOWN)

        except:
            content = was.response.build_error_template (was.app.debug and sys.exc_info () or None, 0, was = was)
            was.traceback ()

        respond (was, content, True)

    has_hooks = True
    try:
        hooks = was.request._hooks
    except AttributeError:
        hooks = (None, None, None)
        has_hooks = False

    try:
        depends = was.request._depends
    except AttributeError:
        depends = []

    if not has_hooks and not depends:
        return respond (was, content)

    was.thread_executor.submit (postprocess, was, content, exc_info, depends, hooks)


# add late response methods --------------------------
if not hasattr (tasks.Future, "_get_was"):
    for cls in (tasks.Future, tasks.Futures, tasks.Tasks, tasks.Mask, pth_task.Task, sp_task.Task):
        for meth in ('_get_was', '_late_respond'):
            setattr (cls, meth, getattr (ResponsibleTask, meth))


