import sys
import os
import socket
import struct
import json
import time
import logging

logger = logging.getLogger(__name__)

class DiscordIPC:
    def __init__(self):
        self.path = self._get_ipc_path()
        self.pipe = None
        self.connect()

    def _get_ipc_path(self):
        if sys.platform == 'win32':
            return r'\\?\pipe\discord-ipc-0'
        return os.path.join(os.environ.get('XDG_RUNTIME_DIR', '/tmp'), 'discord-ipc-0')

    def connect(self):
        try:
            if sys.platform == 'win32':
                self.pipe = open(self.path, 'w+b', buffering=0)
            else:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(self.path)
                self.pipe = sock.makefile('rwb')
            logger.info("[IPC] Connected to Discord IPC")
        except Exception as e:
            logger.error(f"[IPC] Connection failed: {e}")
            self.pipe = None

    def send(self, op: int, payload: dict):
        if not self.pipe:
            return
        try:
            data = json.dumps(payload).encode('utf-8')
            header = struct.pack('<II', op, len(data))
            self.pipe.write(header + data)
            self.pipe.flush()
        except Exception as e:
            logger.warning(f"[IPC] Send failed: {e}")
            self.pipe = None

    def receive(self):
        try:
            header = self.pipe.read(8)
            if len(header) < 8:
                return None, None
            op, length = struct.unpack('<II', header)
            data = self.pipe.read(length)
            return op, json.loads(data.decode('utf-8'))
        except Exception as e:
            logger.warning(f"[IPC] Receive failed: {e}")
            self.pipe = None
            return None, None

    def close(self):
        if self.pipe:
            try:
                self.pipe.close()
                logger.info("[IPC] Pipe closed")
            except Exception as e:
                logger.warning(f"[IPC] Close failed: {e}")
            self.pipe = None
