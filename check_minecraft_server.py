"""
A Python script meant to be run on a Linux machine that's running a Minecraft server. Checks every
LOOP_DELAY seconds if the Minecraft server has any online players. If not, it will wait
SHUTDOWN_DELAY seconds and then shut down the whole Linux server.

Needs the following python libraries:
* mcstatus
"""
import argparse
import subprocess
from datetime import datetime, timedelta
from time import sleep
from typing import Optional

from mcstatus import JavaServer

SHUTDOWN_DELAY = 5 * 60
LOOP_DELAY = 30


def main(port: int):
    last_active_player_time = datetime.now()
    try:
        while True:
            player_count = get_online_player_count(port)
            if player_count is not None and player_count > 0:
                last_active_player_time = datetime.now()
            elif player_count == 0 and last_active_player_time:
                if datetime.now() > last_active_player_time + timedelta(seconds=SHUTDOWN_DELAY):
                    print("Stopping minecraft server...")
                    stop_minecraft_server()
                    return
            sleep(LOOP_DELAY)
    except KeyboardInterrupt:
        pass


def get_online_player_count(port: int) -> Optional[int]:
    try:
        address = f"localhost:{port}"
        server = JavaServer.lookup(address)
        status = server.status()
        print(f"The server has {status.players.online} player(s) online and replied in {status.latency:.02f} ms")
        return status.players.online
    except (OSError, TimeoutError, ConnectionRefusedError) as e:
        print(f"{e.__class__.__name__}: {e}")
        return None


def stop_minecraft_server():
    # subprocess.Popen(["sudo", "shutdown", "-h", "now"])
    print(subprocess.Popen(["gcloud", "compute", "instances", "stop", "minecraft-server-spot", "--zone=us-west1-a"]))


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("port", type=int, help="Port the minecraft server is listening for traffic on")
    return args.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.port)
