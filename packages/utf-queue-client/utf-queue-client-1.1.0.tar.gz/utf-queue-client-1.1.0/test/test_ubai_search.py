from utf_queue_client.scripts.ubai_search_cli import cli
from utf_queue_client.clients import create_span_decorator
import os
import subprocess
import sys

span_decorator = create_span_decorator()

@span_decorator
def test_ubai_search_cli():
    metadata = [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "ble"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
    ]

    results = cli("test", ".hex", metadata)
    assert len(results) == 1


@span_decorator
def test_ubai_search_cli_script():
    metadata = [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "ble"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
    ]

    args = ["--name", "test", "--extension", ".hex"]
    for k, v in metadata:
        args += ["--metadata", k, v]
    process = subprocess.Popen(
        [
            sys.executable,
            os.path.join("utf_queue_client", "scripts", "ubai_search_cli.py"),
        ]
        + args,
        stdout=subprocess.PIPE,
    )
    output, _ = process.communicate()
    assert process.poll() == 0
    assert output.decode().strip() == "15d8ebfd-4c14-4d95-b21c-a73a76f1f3a5"
