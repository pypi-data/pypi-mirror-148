import pytest
from cleo import CommandTester


@pytest.mark.parametrize(
    "commandline", [("-s my_container"), ("-u my_new_container"), ("-m my_container")]
)
def test_get_accounts_command(cmd_app, commandline):
    command = cmd_app.find("accounts")
    command_tester = CommandTester(command)
    command_tester.execute(commandline)

    assert command_tester.io.fetch_output() is not None
