from typing import Awaitable, Callable, Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import globals


class App(FastAPI):

    def on_connect(self, handler: Union[Callable, Awaitable]) -> None:
        """Called every time a new client connects to NiceGUI.

        The callback has an optional parameter of `nicegui.Client`.
        """
        globals.connect_handlers.append(handler)

    def on_disconnect(self, handler: Union[Callable, Awaitable]) -> None:
        """Called every time a new client disconnects from NiceGUI.

        The callback has an optional parameter of `nicegui.Client`.
        """
        globals.disconnect_handlers.append(handler)

    def on_startup(self, handler: Union[Callable, Awaitable]) -> None:
        """Called when NiceGUI is started or restarted.

        Needs to be called before `ui.run()`.
        """
        if globals.state == globals.State.STARTED:
            raise RuntimeError('Unable to register another startup handler. NiceGUI has already been started.')
        globals.startup_handlers.append(handler)

    def on_shutdown(self, handler: Union[Callable, Awaitable]) -> None:
        """Called when NiceGUI is shut down or restarted.

        When NiceGUI is shut down or restarted, all tasks still in execution will be automatically canceled.
        """
        globals.shutdown_handlers.append(handler)

    async def shutdown(self) -> None:
        """Programmatically shut down NiceGUI.

        Only possible when auto-reload is disabled.
        """
        if globals.reload:
            raise Exception('calling shutdown() is not supported when auto-reload is enabled')
        globals.server.should_exit = True

    def add_static_files(self, path: str, directory: str) -> None:
        """Add static files.

        `add_static_files()` makes a local directory available at the specified endpoint, e.g. `'/static'`.
        This is useful for providing local data like images to the frontend.
        Otherwise the browser would not be able to access the files.
        Do only put non-security-critical files in there, as they are accessible to everyone.

        :param path: string that starts with a slash "/"
        :param directory: folder with static files to serve under the given path
        """
        globals.app.mount(path, StaticFiles(directory=directory))
