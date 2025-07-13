import os
import time
import threading
import logging
from .ipc import DiscordIPC
from .config import Config

logger = logging.getLogger(__name__)

class DiscordRPC:
    def __init__(self, config: Config):
        self.config = config
        self.ipc = DiscordIPC()
        self.running = False
        self.heartbeat_thread = None
        self.watch_thread = None

    def handshake(self):
        self.ipc.send(0, {"v": 1, "client_id": self.config.client_id})
        op, resp = self.ipc.receive()
        logger.info("[Handshake] %s", resp)

    def _activity_payload(self):
        activity = {
            "state": self.config.state,
            "details": self.config.details,
            "assets": {
                "large_image": self.config.large_image,
                "large_text": self.config.large_text
            }
        }

        if self.config.enable_timestamp:
            activity["timestamps"] = {"start": self.config.timestamp or int(time.time())}

        return {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": os.getpid(),
                "activity": activity
            },
            "nonce": str(time.time())
        }

    def set_activity(self):
        payload = self._activity_payload()
        self.ipc.send(1, payload)
        logger.info("[Activity Set]")

    def heartbeat_loop(self):
        while self.running:
            time.sleep(15)
            try:
                self.ipc.send(1, {"cmd": "PING", "nonce": str(time.time())})
                logger.debug("[Heartbeat Sent]")
            except Exception as e:
                logger.warning(f"[Heartbeat Error] {e}")
                self.ipc.connect()
                self.handshake()
                self.set_activity()

    def watch_config(self):
        while self.running:
            time.sleep(2)
            if self.config.reload():
                logger.info("[Config Reloaded] Updating Activity")
                self.set_activity()

    def run(self):
        self.running = True
        self.handshake()
        self.set_activity()

        self.heartbeat_thread = threading.Thread(target=self.heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

        self.watch_thread = threading.Thread(target=self.watch_config, daemon=True)
        self.watch_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            self.ipc.close()
            logger.info("[Disconnected]")
