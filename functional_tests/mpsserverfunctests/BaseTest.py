import unittest

import aiounittest as aiounittest
import requests
import time
import json
import logging

PORT = 7994
BASE_URL = "http://localhost:%d" % PORT
BASE_WS_URL_CUSTOM = "ws://localhost:%d/socket" % PORT
BASE_WS_URL_JSONRPC = "ws://localhost:%d/jsonrpc" % PORT
MODEL_SERVER_URL = "http://localhost:7777"


class BaseAsyncTest(aiounittest.AsyncTestCase):

    async def _get_response(self, websocket):
        try:
            response = json.loads(await websocket.recv())
            if 'type' in response and response['type'] == 'KeepAlive':
                return await self._get_response(websocket)
            if 'result' in response and 'type' in response['result'] and response['result']['type'] == 'KeepAlive':
                return await self._get_response(websocket)
            return response
        except Exception as e:
            raise Exception("Could not obtain answer") from e

    @classmethod
    def try_to_connect(cls, attempts_left=65):
        log = cls.getLogger()
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                log.debug(f"{cls.classSignaturePrefix()} [connected to MPSServer]")
                return True
            else:
                print("status code: %d" % r.status_code)
                return False
        except Exception:
            if attempts_left > 0:
                log.debug(f"  {cls.classSignaturePrefix()} attempts left: %d" % attempts_left)
                time.sleep(5)
                return cls.try_to_connect(attempts_left - 1)
            else:
                raise Exception("Too many attempts, giving up")

    @classmethod
    def classSignaturePrefix(cls):
        return f"(test class {cls.__name__})"

    @classmethod
    def getLogger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def setUpClass(cls):
        log = cls.getLogger()
        log.debug(f"{cls.classSignaturePrefix()} Waiting for MPSServer to be up...")
        if not cls.try_to_connect():
            raise Exception("Initialization failed")


class BaseTest(unittest.TestCase):
    @classmethod
    def getLogger(cls):
        return logging.getLogger(cls.__name__)

    @classmethod
    def try_to_connect(cls, attempts_left=65):
        log = cls.getLogger()
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                log.debug(f"{cls.classSignaturePrefix()} [connected to MPSServer]")
                return True
            else:
                log.debug("status code: %d" % r.status_code)
                return False
        except Exception:
            if attempts_left > 0:
                log.debug(f"  {cls.classSignaturePrefix()} attempts left: %d" % attempts_left)
                time.sleep(5)
                return cls.try_to_connect(attempts_left - 1)
            else:
                raise Exception("Too many attempts, giving up")

    @classmethod
    def classSignaturePrefix(cls):
        return f"(test class {cls.__name__})"

    @classmethod
    def setUpClass(cls):
        log = cls.getLogger()
        log.debug(f"{cls.classSignaturePrefix()} Waiting for server to be up...")
        if not cls.try_to_connect():
            raise Exception("Initialization failed")
