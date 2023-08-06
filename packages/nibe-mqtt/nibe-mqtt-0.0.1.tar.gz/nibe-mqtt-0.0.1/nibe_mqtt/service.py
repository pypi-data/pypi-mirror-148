import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

from nibe.coil import Coil
from nibe.connection.nibegw import NibeGW
from nibe.exceptions import CoilWriteException
from nibe.heatpump import HeatPump
from nibe_mqtt import cfg
from nibe_mqtt.mqtt import MqttConnection, MqttHandler
from slugify import slugify

logger = logging.getLogger("nibe").getChild(__name__)


class PollService:
    LAST_UPDATE_ATTR = "last_update"

    def __init__(self, heatpump: HeatPump, connection: NibeGW, conf: dict):
        self._connection = connection
        self._heatpump = heatpump

        self._interval = conf["interval"]
        self._coils = [self._get_coil(key) for key in conf["coils"]]

    def _get_coil(self, name_or_address: Union[str, int]):
        if isinstance(name_or_address, str):
            return self._heatpump.get_coil_by_name(name_or_address)
        if isinstance(name_or_address, int):
            return self._heatpump.get_coil_by_address(name_or_address)

    def start(self):
        asyncio.create_task(self._loop())

    async def _loop(self):
        await asyncio.sleep(self._interval)
        while True:
            await asyncio.sleep(5.0)
            for coil in self._coils:
                last_update = getattr(coil, self.LAST_UPDATE_ATTR, None)
                if (
                    last_update is None
                    or last_update + timedelta(seconds=self._interval) < datetime.now()
                ):
                    logger.info(
                        f"Polling coil {coil.name}: last_update = {last_update}"
                    )
                    try:
                        await self._connection.read_coil(coil)
                    except Exception as e:
                        logger.warning(f"Poll {coil.name} failed: {e}")

    def register_update(self, coil: Coil):
        setattr(coil, self.LAST_UPDATE_ATTR, datetime.now())


class Service(MqttHandler):
    def __init__(self, conf: dict):
        self.conf = conf
        self.heatpump = HeatPump(conf["nibe"]["model"])
        self.heatpump.initialize()
        self.announced_coils = set()

        self.heatpump.subscribe(HeatPump.COIL_UPDATE_EVENT, self.on_coil_update)

        self.connection = NibeGW(
            heatpump=self.heatpump,
            listening_ip=conf["nibe"]["nibegw"]["listening_ip"],
            listening_port=conf["nibe"]["nibegw"]["listening_port"],
            remote_ip=conf["nibe"]["nibegw"]["ip"],
            remote_read_port=conf["nibe"]["nibegw"]["read_port"],
            remote_write_port=conf["nibe"]["nibegw"]["write_port"],
        )

        self.poller = None
        poll_config = conf["nibe"].get("poll")
        if poll_config is not None:
            self.poller = PollService(self.heatpump, self.connection, poll_config)

        self.mqtt_client = MqttConnection(self, conf["mqtt"])

    def _get_device_info(self) -> dict:
        return {
            "model": self.conf["nibe"]["model"].name,
            "name": "Nibe heatpump integration",
            "id": slugify("Nibe " + self.conf["nibe"]["nibegw"]["ip"]),
        }

    def handle_coil_set(self, name, value: str):
        coil = self.heatpump.get_coil_by_name(name)
        try:
            coil.value = value

            asyncio.create_task(self._write_coil(coil))
        except AssertionError as e:
            logger.error(e)
        except Exception as e:
            logger.exception("Unhandled exception", e)

    async def _write_coil(self, coil):
        try:
            coil_value = coil.value
            await self.connection.write_coil(coil)
            if (
                coil_value == coil.value
            ):  # if coil value did not change while we were writing, just publish to MQTT
                self.on_coil_update(coil)
            else:  # if value has changed we do not know what is the current state
                logger.info(
                    f"{coil.name} value has changed while we were writing: {coil_value} -> {coil.value}. Requesting new update"
                )
                await self.connection.read_coil(coil)
        except CoilWriteException as e:
            logger.error(e)
        except Exception as e:
            logger.exception("Unhandled exception", e)

    async def start(self):
        await self.connection.start()

        self.mqtt_client.start()

        if self.poller is not None:
            self.poller.start()

    def on_coil_update(self, coil: Coil):
        if coil not in self.announced_coils:
            self.mqtt_client.publish_discovery(coil, self._get_device_info())
            self.announced_coils.add(coil)

        self.mqtt_client.publish_coil_state(coil)

        if self.poller is not None:
            self.poller.register_update(coil)


if __name__ == "__main__":
    conf = cfg.load(Path("config.yaml"))

    service = Service(conf)

    logging.basicConfig(**conf["logging"])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(service.start())
    loop.run_forever()
