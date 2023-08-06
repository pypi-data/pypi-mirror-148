import pytest

from utf_queue_client.scripts.ubai_upload_cli import cli
from utf_queue_client.clients import create_span_decorator
import os
import subprocess
import sys

span_decorator = create_span_decorator()


@pytest.fixture
def metadata():
    yield [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "ble"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
    ]


@span_decorator
def test_ubai_upload_cli(request, metadata):
    file = os.path.join(os.path.dirname(__file__), "test.hex")

    username = os.environ["UTF_QUEUE_USERNAME"]
    password = os.environ["UTF_QUEUE_PASSWORD"]
    client_id = request.node.name
    cli(file, metadata, username, password, client_id)


@span_decorator
def test_ubai_upload_cli_script(request, metadata):
    file = os.path.join(os.path.dirname(__file__), "test.hex")

    client_id = request.node.name
    args = ["--file-path", file, "--client-id", client_id]
    for k, v in metadata:
        args += ["--metadata", k, v]
    process = subprocess.Popen(
        [
            sys.executable,
            os.path.join("utf_queue_client", "scripts", "ubai_upload_cli.py"),
        ]
        + args,
    )
    process.communicate()
    assert process.poll() == 0
