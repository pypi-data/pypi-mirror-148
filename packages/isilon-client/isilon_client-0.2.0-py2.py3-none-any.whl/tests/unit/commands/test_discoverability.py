from cleo import CommandTester


def test_discoverability_command(cmd_app):
    command = cmd_app.find("discoverability")
    command_tester = CommandTester(command)
    command_tester.execute()

    assert command_tester.io.fetch_output() is not None
