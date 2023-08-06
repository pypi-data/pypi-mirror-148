from cleo import CommandTester


def test_endpoints_command(cmd_app):
    command = cmd_app.find("endpoints")
    command_tester = CommandTester(command)
    command_tester.execute()

    assert command_tester.io.fetch_output() is not None
