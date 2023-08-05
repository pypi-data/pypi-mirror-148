from pathlib import Path
from shutil import rmtree

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from huawei_lte_api.enums.device import ControlModeEnum

from serialix import Serialix


LOCAL_CONFIG_PATH = Path.home() / Path('.config/hurocon/config.json')
LOCAL_CONFIG_DEFAULT = {
    "config_version": 1,
    "connection_ip": "192.168.8.1",
    "auth": {
        "username": "admin",
        "password": "admin"
    }
}


class LocalConfig(Serialix):
    def __new__(self, **kwargs):
        return super().__new__(
            self, 'json',
            LOCAL_CONFIG_PATH, LOCAL_CONFIG_DEFAULT,
            parser_write_kwargs={"indent": 4},
            **kwargs
        )


class HLC_Connection(Connection):
    def __init__(self):
        cfg = LocalConfig()
        super().__init__(
            url='http://{}/'.format(cfg['connection_ip']),
            username=cfg['auth']['username'],
            password=cfg['auth']['password']
        )


def test_connection() -> str:
    """
    Test connection to router with details from configuration file

    :return: "ok" if successfully connected or the reason of failure
    :rtype: str
    """
    result = 'ok'
    try:
        with HLC_Connection() as router_con:
            Client(router_con)
    except Exception as e:
        result = e

    return result


def reboot_router() -> None:
    with HLC_Connection() as router_con:
        client = Client(router_con)
        client.device.set_control(ControlModeEnum.REBOOT)


def sms_send(number, text: str) -> str:
    with HLC_Connection() as router_con:
        return Client(router_con).sms.send_sms(
            [number],
            text
        )


def set_auth_details(username: str, password: str) -> None:
    cfg = LocalConfig()
    cfg['auth']['username'] = username
    cfg['auth']['password'] = password
    cfg.commit()


def set_connection_details(ip: str) -> None:
    cfg = LocalConfig()
    cfg['connection_ip'] = ip
    cfg.commit()


def reset_auth_details() -> None:
    cfg = LocalConfig()
    cfg['auth'] = LOCAL_CONFIG_DEFAULT['auth']
    cfg.commit()


def erase_config() -> bool:
    """
    Erase all local configuration files and dirs

    :return: Do the existing file was successfully removed
    :rtype: bool
    """
    result = False

    if LOCAL_CONFIG_PATH.parent.exists():
        rmtree(LOCAL_CONFIG_PATH.parent)
        result = True

    return result
