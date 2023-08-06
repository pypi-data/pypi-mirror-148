import pytest
from cleo import CommandTester


@pytest.mark.parametrize(
    "commandline,expected",
    [
        # ("my_container my_object", "my_object object saved.\n"),
        ("-c my_container my_object --data README.md", "my_object object created.\n"),
        # ("-m my_container my_object", "X-Object-Meta: mock\n"),
        ("-u my_container my_object", "metadata updated.\n"),
        ("-d my_container my_object", "my_object object deleted.\n"),
    ],
)
def test_get_objects_command(cmd_app, commandline, expected):
    command = cmd_app.find("objects")
    command_tester = CommandTester(command)
    command_tester.execute(commandline)

    assert command_tester.io.fetch_output() == expected


def test_get_objects_command_error(cmd_app):
    command = cmd_app.find("objects")
    command_tester = CommandTester(command)
    with pytest.raises(SystemExit):
        command_tester.execute("-c my_container my_object")
