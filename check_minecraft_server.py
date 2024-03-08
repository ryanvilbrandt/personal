"""
Needs the following python libraries:
* mcstatus
* google-cloud-compute
"""

import os
import sys
from json import loads
from typing import Any, Optional

from google.api_core.extended_operation import ExtendedOperation
from google.cloud.compute_v1 import InstancesClient
from google.oauth2.service_account import Credentials
from mcstatus import JavaServer

address = os.environ["MINECRAFT_SERVER_ADDRESS"]
GOOGLE_SHEETS_SERVICE_ACCOUNT = loads(os.environ["MINECRAFT_VM_SERVICE_ACCOUNT"])


def main():
    if get_online_player_count() == 0:
        print("Stopping minecraft server...")
        print(stop_minecraft_server())


def get_online_player_count() -> Optional[int]:
    try:
        server = JavaServer.lookup(address)
        status = server.status()
        print(f"The server has {status.players.online} player(s) online and replied in {status.latency:.02f} ms")
        return status.players.online
    except (TimeoutError, ConnectionRefusedError):
        print("Server is not running, or didn't respond.")
        return None


def stop_minecraft_server():
    stop_instance(
        os.environ["MINECRAFT_PROJECT_ID"],
        os.environ["MINECRAFT_PROJECT_ZONE"],
        os.environ["MINECRAFT_VM_NAME"],
    )


# Taken from https://cloud.google.com/compute/docs/samples/compute-stop-instance#compute_stop_instance-python
def stop_instance(project_id: str, zone: str, instance_name: str) -> None:
    """
    Stops a running Google Compute Engine instance.
    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance your want to stop.
    """
    creds = Credentials.from_service_account_info(GOOGLE_SHEETS_SERVICE_ACCOUNT)
    instance_client = InstancesClient(credentials=creds)

    operation = instance_client.stop(
        project=project_id, zone=zone, instance=instance_name
    )
    return wait_for_extended_operation(operation, "instance stopping")


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    Waits for the extended (long-running) operation to complete.

    If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


if __name__ == '__main__':
    main()
