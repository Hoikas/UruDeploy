#    This file is part of UruDeploy.
#
#    UruDeploy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    UruDeploy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with UruDeploy.  If not, see <http://www.gnu.org/licenses/>.

import abc
import multiprocessing

class BuildProcess:
    def __init__(self):
        self._async_handle = None

    @property
    def supports_async(self):
        """This builder can be executed asynchronously"""
        # All should be able to, TBH
        return True

    @abc.abstractmethod
    def run(self):
        pass

    def start(self):
        """Starts this builder in blocking mode"""
        self.run()

    def start_async(self):
        """Starts this builder without blocking execution
           NOTE: The derived builder MUST be able to execute it its own process!
        """
        if not self.supports_async:
            raise RuntimeError("Builder '{}' cannot be executed asynchronously!".format(self.__class__.__name__))

        # As much as I like the GIL, there's really no need for us to share resources.
        # The only limitation here is stuff like sharing fds, but that shouldn't be a prob here
        self._async_handle = multiprocessing.Process(target=self.run)
        self._async_handle.start()

    def join(self):
        """Waits for the asynchronous process to finish"""
        if self._async_handle is not None:
            self._async_handle.join()

