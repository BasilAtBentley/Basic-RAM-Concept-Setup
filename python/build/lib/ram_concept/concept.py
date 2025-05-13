#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import TYPE_CHECKING
import os
from queue import Empty
from queue import Queue
from winreg import OpenKey
import socket
from threading import Thread
import subprocess
import time
import winreg

# THIRD PARTY IMPORTS
import requests

# INTERNAL (THIS LIBRARY) IMPORTS
from .api_version import api_version
from .api_version import _matching_registry_exe_version
from .bracket_parser import BracketParser
from .model import Model

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    pass

# -------------------------------------------------------------------------------------------------

# Good info on the requests library https://requests.readthedocs.io/en/master/
# and https://realpython.com/python-requests/

# -------------------------------------------------------------------------------------------------

class Concept:
    """Concept represents the RAM Concept process that hosts the data ("file").

    A maximum of 1 Model may be managed by a Concept process at anytime. However, there can be multiple
    Concept processes active (which indirectly allows multiple Models to be active).
    
    This class should not be subclassed.
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_default_timeout_seconds",
        "_model",
        "_url",
        "_nextRequestId"
    ]

    # CONSTRUCTION

    def __init__(self, url: str):
        """Initializes this to use the given URL to contact the Concept process.

        The url should be in the form 'http://localhost:1999/'."""
        super().__init__()
        self._url = url
        self._model = None
        self._nextRequestId = 1

        # timeout is problemmatic as some operations take a long time
        self._default_timeout_seconds = 1 * 60 * 60 # 1 hour for now....

        # reality check that the concept process will at least respond to ping
        response = self.ping(10)
        if(response != "PONG"):
            raise Exception("Unexpected [PING] response: '" + response + "'")

    # PUBLIC CREATION OPERATIONS

    @staticmethod
    def attach_to_concept(port: int) -> Concept:
        """Attaches to an existing RAM Concept that will serve this API.

        The caller is responsible for having started the Concept process listening to the given port.

        Concept should have been started with the command:

        `concept.exe -apiServer -port <port_number> -inactivityTimeout <timeout_in_seconds> -version <api_version>`

        `port_number` is in the 1..65535 range; `api_version` has the format 8.2.1

        This method is not commonly used.

        Parameters
        ----------
        port
            The port number for the server to use

        Returns
        -------
        Concept
            A Concept object, ready for use.
        """

        # The url should be in the form 'http://localhost:1999/'
        url = "http://localhost:" + str(port) + "/"
        return Concept(url)

    @staticmethod
    def start_concept(headless: bool = True, path: str = None, port: int = None, start_timeout_seconds: int = None, inactivity_timeout_seconds: int = None, log_file_path: str = None) -> Concept:
        """Start the RAM Concept server that will serve this API.

        Parameters
        ----------
        headless
            true to run the server headlessly, false to run the server with a GUI
        path
            path to the RAM Concept exe to start (if None, default location will be used)
        port
            The port number for the server to use (if None, an available port will be used)
        start_timeout_seconds
            The number of seconds to allow the server to start up before timing out (if None, a default value is used)
        inactivity_timeout_seconds
            The number of seconds that the server will wait for the next API command before timing out (if None, a default value is used)
        log_file_path
            Path to a log file that is written to by the RAM Concept.exe (rarely used)

        Returns
        -------
        Concept
            A Concept object, ready for use.
        """
        try:
            return Concept._start_concept(headless, path, port, start_timeout_seconds, inactivity_timeout_seconds, log_file_path)
        except:
            # if port is None we try this twice just to handle the extremely unlikely case of
            # the port determined being taken (see _find_available_port for race condition details)
            if port == None:
                return Concept._start_concept(headless, path, port, start_timeout_seconds, inactivity_timeout_seconds, log_file_path)
            else:
                raise
    

    def shut_down(self) -> None:
        """Shutdown the associated Concept process. This and any related Model become unusable."""
        self._close_any_open_model()
        
        response = self._command("[SHUT_DOWN]")
        if response != "SHUTTING_DOWN":
            raise Exception("Unexpected response from SHUT_DOWN command: " + response)

        self._url = None



    # MODEL-RELATED OPERATIONS

    def open_file(self, file_path: str) -> Model:
        """Open the file in the RAM Concept process and create a Model representing it.

        Any currently open file is closed, and related Models become unusable.

        Parameters
        ----------
        file_path
            full path to the RAM Concept file to open

        Returns
        -------
        Model
            The Model representing the file, ready for use.
        """
        self._close_any_open_model()

        self._command("[OPEN_FILE][" + file_path + "]") # throws or succeeds...

        self._model = Model(self)
        return self._model


    def new_model(self) -> Model:
        """Create a new unsaved "file" in the RAM Concept process and create a Model representing it.

        Any currently open file is closed, and related Models become unusable.

        Returns
        -------
        Model
            The Model representing the (unsaved) file, ready for use.
        """
        self._close_any_open_model()
        self._command("[NEW_MODEL]") # throws or succeeds...
        self._model = Model(self)
        return self._model

    # INTERNAL MODEL-RELATED OPERATIONS

    def _close_any_open_model(self) -> None:
        """Close any open model (file) and make that Model unusable.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.
        """
        if self._model != None:
            self._model.close_model()
            assert self._model == None # close_model should indirectly to that
            self._model = None

    def _model_closed(self, model: Model) -> None:
        """Update internal state to reflect that the model has closed.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.
        
        Parameters
        ----------
        model
            The Model that was closed (must be currently active model for this Concept)
        """
        if(model != self._model):
            raise Exception("model is not currently active Model for this Concept.")

        self._model = None


    # OTHER COMMANDS

    def ping(self, timeout_seconds: int = None) -> str:
        """Send the [PING] command to the RAM Concept process.

        The expected response is "PONG".
        
        Parameters
        ----------
        timeout_seconds
            The number of seconds to wait for a response before timing out (if None, default value is used)

        Returns
        -------
        str
            The response to the [PING] command (expected to be "PONG").
        """
        return self._command('[PING]', timeout_seconds)

    def _get_process_id(self) -> int:
        """Send the [GET_PROCESS_ID] command to the RAM Concept process.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.

        Returns
        -------
        int
            the process id of the concept process serving the API
        """
        response = self._command('[GET_PROCESS_ID]')
        process_id = int(response)
        return process_id


    # INTERNAL CORE COMMAND OPERATION

    def _command(self, cmd: str, timeout_seconds: int = None) -> str:
        """Send the command to the RAM Concept process.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.
        
        Parameters
        ----------
        cmd
            The command to execute. Must be in bracket string format.
        timeout_seconds
            The number of seconds to wait for a response before timing out (if None, default value is used)

        Returns
        -------
        str
            The response to the command.
        """
        if(timeout_seconds is None):
            timeout_seconds = self._default_timeout_seconds

        requestId = self._nextRequestId
        self._nextRequestId += 1

        utf8_cmd = cmd.encode(encoding="utf-8")
        response = requests.post(self._url, headers = {'Content-Type': 'text/plain;charset=UTF-8', 'RequestId' : str(requestId)}, data=utf8_cmd, timeout=timeout_seconds)

        # if some protocol or network issue occurs, we just pass that on.
        response.raise_for_status()

        # the result should be in one of two formats:
        #   [SUCCESS][response]
        #   [FAILURE][response]
        result = response.text

        # REDO THIS WITH BRACKET STRING PARSER
        prefix = result[:10]
        if prefix == '[SUCCESS][':
            return result[10:-1]
        elif prefix ==  '[FAILURE][':
            raise Exception('Error: {0}'.format(result[10:-1]))
        else:
            raise Exception('Internal Error: Invalid result returned from Concept process: {0}'.format(result))
        
    # INTERNAL CONCEPT SERVER STARTUP OPERATIONS

    @staticmethod
    def _stdout_to_queue(process: subprocess.Popen, queue: Queue)->None:
        """Takes the stdout from the given process and puts it in the queue.
        This is a helper for _start_concept and is designed to run in a background thread.
        See also: https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
        """
        # we expect only a single stdout response from the concept.exe.
        # the count logic here is only intended to protect against some unforeseen circumstance where a concept.exe process
        # sends back a long series of responses that potentially all get stored in the queue creating a large memory leak
        # (perhaps the host script has given up on this process and started a second concept.exe process)
        count = 0
        for line in iter(process.stdout.readline, b''):
            count += 1
            if count > 100:
                pass
            else:
                queue.put(line)
        process.stdout.close()

    @staticmethod
    def _start_concept(headless: bool, path: str = None, port: int = None, start_timeout_seconds: int = None, inactivity_timeout_seconds: int = None, log_file_path: str = None) -> Concept:
        """Start the RAM Concept server that will serve this API.

        Parameters
        ----------
        path
            path to the RAM Concept exe to start (if None, default location will be used)
        port
            The port number for the server to use (if None, an available port will be used)
        start_timeout_seconds
            The number of seconds to allow the server to start up before timing out (if None, a default value is used)
        inactivity_timeout_seconds
            The number of seconds that the server will wait for the next API command before timing out (if None, a default value is used)

        Returns
        -------
        Concept
            A Concept object, ready for use.
        """
        if(path is None):
            path = Concept._find_concept_path()

        if(port is None):
            port = Concept._find_available_port()

        if(start_timeout_seconds is None):
            start_timeout_seconds = 60

        if(inactivity_timeout_seconds is None):
            inactivity_timeout_seconds = 1 * 60 * 60 # 1 hour

        if headless:
            command = "-apiServer"
        else:
            command = "-apiServerWithGui"

        args = [path, command, "-version", api_version(), "-port", str(port), "-inactivityTimeout", str(inactivity_timeout_seconds)]
        if not (log_file_path is None):
            args.append("-log")
            args.append(log_file_path)

        # Popen can fail in these ways:
        #    FileNotFoundError raised if the exe file does not exist
        #    OSError raised if the exe is not a valid Win32 application
        process = subprocess.Popen(args,stdout=subprocess.PIPE, text=True)

        # check for some kind of immediate failure to launch that doesn't raise an exception
        # this logic is somewhat unnecessary as the failure will eventually get caught below
        # but this case will allow catching the return code
        time.sleep(2)
        return_code = process.poll()
        if return_code != None:
            raise Exception("RAM Concept process exited unexpectedly with return code " + str(return_code) + ".")

        # start a background thread to fill the queue from process.stdout
        # this background thread queue strategy from: https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
        queue = Queue()
        queue_thread = Thread(target=Concept._stdout_to_queue, args=(process, queue))
        queue_thread.daemon = True # die when this process closes, but don't prevent this process from closing
        queue_thread.start()

        # wrap this in try/except to be able to kill server process if something fails
        try:

            # wait until concept server is running
            startup_time_limit = time.monotonic() + start_timeout_seconds
            while True:
                try:
                    line = queue.get_nowait().rstrip()
                except Empty:
                    pass
                else: # line was read
                    if (line == "[SERVER_START_SUCCESS]"):
                        break # success!

                    elif (line.startswith("[SERVER_START_FAILURE]")):
                        tokens = BracketParser.parse(line)
                        # expect 2 tokens
                        raise Exception("Server startup failed: " + tokens[1])

                    else: # unexpected case
                        # This case has occurred, but we have not been able to reproduce it under debug conditions.
                        # When it has happens, the pipe appears to return a series of blank lines.
                        # It might happen when there is sufficient permission to start the process, but not read from the pipe?
                        # Decided to leave this print in for diagnostic purposes (field or developer)
                        print("Unexpected response from stdout: " + line)

                if(time.monotonic() > startup_time_limit):
                    raise Exception("Could not start RAM Concept in timeout period.")

                time.sleep(0.5)
            
            # if we get here, we have a responsive process (at least responsive through stdout)
            url = "http://localhost:" + str(port) + "/"
            concept = Concept(url)

            ping_timeout = 10 # seconds (seems extraordinarily, long....but maybe some startup logic would be slow)
            response = concept._command("[PING]", ping_timeout) # will raise exception if timeout exceeded
            if response != "PONG":
                raise Exception("Unexpected response from server PING: " + response)

            # we have a fully functional server!
            return concept
        except:
            process.kill()
            raise



    @staticmethod
    def _find_available_port() -> int:
        """Find an available port to use with localhost.

        While the port is available at the time of the call, it could be taken (by another process) immediately thereafter.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.

        Returns
        -------
        int
            The available port.
        """
        temp_socket = socket.socket()
        temp_socket.bind(("",0))
        port = temp_socket.getsockname()[1]
        temp_socket.close()

        return int(port)


    @staticmethod
    def _find_concept_path() -> str:
        """Find the path to an appropriate RAM Concept to user for a server.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.
        
        Returns
        -------
        str
            Full path to the RAM Concept exe
        """
        
        # return Concept._find_debug_concept_path()
        return Concept._find_release_concept_path()

    # @staticmethod
    # def _find_debug_concept_path() -> str:
    #     """Find the path to an appropriate RAM Concept to use for a server when debugging.

    #     THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.
        
    #     Returns
    #     -------
    #     str
    #         Full path to the RAM Concept exe
    #     """

    #     # for now, we use the dev exe
    #     out_dir = os.environ.get("OutRoot")
    #     if out_dir is None:
    #         raise Exception("OutRoot not defined")
        
    #     assert out_dir.endswith("\\")

    #     concept_path = out_dir + "Winx64\\Product\\RamConcept\\Prog\\Concept.exe"
    #     if not os.path.isfile(concept_path):
    #         raise Exception("No Concept.exe at: " + concept_path)

    #     return concept_path

    @staticmethod
    def _find_release_concept_path() -> str:
        """Find the path to an appropriate RAM Concept to use for a server when releasing.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.
        
        Returns
        -------
        str
            Full path to the RAM Concept exe
        """
        try:
            path = r"Software\Bentley\Engineering\Concept\Integration"
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)

            # get the path
            path_key_name = "LatestConceptExePath"
            path_value, path_registry_type = winreg.QueryValueEx(registry_key, path_key_name)
            if path_registry_type != winreg.REG_SZ:
                raise Exception("SOFTWARE\\Bentley\\Engineering\\Concept\\Integration\\LatestConceptExePath is not a registry SZ value")

            # get the version
            # version is a int of the version number * 100: 3.2.1 becomes 321
            version_key_name = "LatestConceptExeVersion"
            version_value, version_registry_type = winreg.QueryValueEx(registry_key, version_key_name)
            if version_registry_type != winreg.REG_DWORD:
                raise Exception("SOFTWARE\\Bentley\\Engineering\\Concept\\Integration\\LatestConceptExeVersion is not a registry DWORD value")

            # version numbers in API look like this "8.2.0"
            # version numbers in registry look like this 820
            required_exe_version_value = _matching_registry_exe_version()
        
            if version_value < required_exe_version_value:
                message = "Concept version {0} or later is required to support scripting API version {0}.".format(api_version())
                raise Exception(message)

            winreg.CloseKey(registry_key)

            return path_value
        except WindowsError:
            # anything we want to do here?
            raise

        

           

