from asyncio import sleep
from os import environ, remove
from pathlib import Path
from shutil import rmtree
from typing import Dict
from zipfile import ZIP_DEFLATED, ZipFile

from aiogram import Bot
from aiogram.types import InputFile
from aiogram.utils.markdown import bold
from paramiko import AutoAddPolicy, SSHClient


class SSH:
    def __init__(
        self,
        host,
        username,
        password: str = None,
        private_key: str = None
    ) -> None:
        self.host = host
        self.username = username
        self.private_key = private_key
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.load_system_host_keys()
        self.client.connect(
            host,
            username=username,
            password=password,
            key_filename=private_key
        )

    def execute(self, command: str) -> str:
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode("utf-8")

    def close(self):
        self.client.close()

    def get_file(self, local_path: str, remote_path: str) -> bool | Exception:
        sftp = self.client.open_sftp()
        try:
            sftp.get(remote_path, local_path)
        except Exception as e:
            return e
        else:
            sftp.close()
            return True

    def get_files(self, paths: Dict[str, str]) -> bool | Exception:
        sftp = self.client.open_sftp()
        try:
            for remote_path, local_path in paths.items():
                if isinstance(local_path, str):
                    sftp.get(remote_path, f'Archives/{local_path}')
                else:
                    Path(f'Archives/{local_path[0]}').mkdir(
                        parents=True, exist_ok=True
                    )
                    sftp.get(
                        remote_path, f'Archives/{local_path[0]}/{local_path[1]}'
                    )
        except Exception as e:
            return e
        else:
            sftp.close()
            return True

    def put_file(self, local_path: str, remote_path: str) -> bool | Exception:
        sftp = self.client.open_sftp()
        try:
            sftp.put(local_path, remote_path)
        except Exception as e:
            return e
        else:
            sftp.close()
            return True


async def create_backup(datetime, bot: Bot) -> str:
    """
    Create backup.
    
    Parameters
    ----------
    datetime: Data e hora.
    """
    archives = {
        'mtasa/mods/deathmatch/internal.db': 'internal.db',
        'mtasa/mods/deathmatch/registry.db': 'registry.db',
        'mtasa/mods/deathmatch/resources/[acc]/LVL/levels.db':
            ['LVL', 'levels.db'],
        'mtasa/mods/deathmatch/resources/[paineis-cliente]/IZ-Vehicle/database.db':
            ['IZ-Vehicle', 'database.db'],
        'mtasa/mods/deathmatch/resources/[acc]/IZ-gpsystem/dbData_byRex.db':
            ['IZ-gpsystem', 'dbData_byRex.db'],
        'mtasa/mods/deathmatch/mtaserver.conf': 'mtaserver.conf',
        'mtasa/mods/deathmatch/acl.xml': 'acl.xml',
        'mtasa/mods/deathmatch/banlist.xml': 'banlist.xml'
    }

    data = datetime.strftime('%d-%m-%Y')
    ssh = SSH(
        host=environ['HOST_BKP'],
        username=environ['USERNAME'],
        private_key='Archives/pkey'
    )
    await bot.send_message(environ['CHATID'], f'=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')
    ssh.get_files(archives)
    ssh.close()
    name = f'Archives/backup_{data}.zip'
    with ZipFile(name, 'w', compression=ZIP_DEFLATED, compresslevel=9) as zip:
        for _, file in archives.items():
            if isinstance(file, str):
                zip.write(f'Archives/{file}')
                remove(f'Archives/{file}')
            else:
                zip.write(f'Archives/{file[0]}/{file[1]}')
                rmtree(f'Archives/{file[0]}')
        zip.close()
    await bot.send_document(environ['CHATID'], InputFile(name))
    data = datetime.strftime('%d/%m/%Y')
    await bot.send_message(
        environ['CHATID'], f'Backup do dia {bold(data)} criado com sucesso !'
    )
    sleep(0.6)
    await bot.send_message(environ['CHATID'], f'=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')
    remove(name)
    return f'Backup criado com sucesso !!\n Data: {data}'
