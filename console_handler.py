import sys

class ConsoleHandler:
    """
    A class to handle console input and execute corresponding commands for the MainFrame.

    Attributes:
        MainFrame: The main frame object that contains the console to append messages and execute commands.
    """

    def __init__(self, MainFrame):
        """
        Initialize the ConsoleHandler class with the specified MainFrame.

        Args:
            MainFrame: The main frame object containing the console.
        """
        self.MainFrame = MainFrame

    def get_console_input(self, text):
        """
        Process the console input text and execute the corresponding command.

        Args:
            text (str): The input text from the console.
        """
        lines = text.split("\n")
        command = self.get_last_non_empty_line(lines)
        if command:
            self.command_list(command)

    def get_last_non_empty_line(self, lines):
        """
        Get the last non-empty line from the provided lines of text.

        Args:
            lines (list): A list of strings representing lines of text.

        Returns:
            list: A list of words from the last non-empty line.
        """
        for line in reversed(lines):
            if line.strip():
                return line.strip().split()

    def command_list(self, commands):
        """
        Execute the command based on the parsed command list.

        Args:
            commands (list): A list of command arguments.
        """
        if not commands:
            return
        elif commands[0] == "Exit":
            sys.exit(0)
        elif commands[0] == "Save":
            if len(commands) > 1:
                if commands[1] == "--all":
                    self.MainFrame.console.append("Saving all\n")
                elif commands[1] == "--mand":
                    self.MainFrame.console.append("Saving Mandelbrot plot\n")
                elif commands[1] == "--log":
                    self.MainFrame.console.append("Saving logistical plot\n")
                else:
                    self.MainFrame.console.append(f"Invalid Save command: {commands[1]}\n")
            else:
                self.MainFrame.console.append("Save command requires an argument\n")
        elif commands[0] == "Refresh":
            if len(commands) > 1:
                if commands[1] == "--all":
                    self.MainFrame.console.append("Refreshing all\n")
                elif commands[1] == "--mand":
                    self.MainFrame.console.append("Refreshing Mandelbrot plot\n")
                elif commands[1] == "--log":
                    self.MainFrame.console.append("Refreshing logistical plot\n")
                else:
                    self.MainFrame.console.append(f"Invalid Refresh command: {commands[1]}\n")
            else:
                self.MainFrame.console.append("Refresh command requires an argument\n")
        elif commands[0] == "Clear":
            if len(commands) > 1:
                if commands[1] == "console":
                    self.MainFrame.console.clear()
                else:
                    self.MainFrame.console.append(f"Invalid Clear command: {commands[1]}\n")
            else:
                self.MainFrame.console.append("Clear command requires an argument\n")
        else:
            self.MainFrame.console.append(f"There is no such command as: {commands[0]}\n")
