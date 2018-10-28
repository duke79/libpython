import os
import signal
import sys
# import cmd2
import cmd


class Shell(cmd.Cmd):
    intro = 'Welcome to shell\n'

    def __init__(self):
        super().__init__()
        self.prompt = os.path.abspath(os.path.curdir) + ">"
        self.history = []

    def default(self, line):  # this method will catch all commands
        # subprocess.call(line, shell=True)
        os.system(line)

    def completedefault(self, text, line, begidx, endidx):
        return [filename for filename in os.listdir('.') if filename.startswith(text)]

    def completenames(self, text, *ignored):
        dotext = 'do_' + text
        commands = [a[3:] for a in self.get_names() if a.startswith(dotext)]
        files = [filename for filename in os.listdir('.') if filename.startswith(text)]
        return commands + files

    def precmd(self, line):
        self.history.append(line)
        return line

    def do_cd(self, line):
        args = str(line).split(" ")
        try:
            os.chdir(args[0])
        except Exception as e:
            print(os.path.abspath(os.path.curdir))
        self.prompt = os.path.abspath(os.path.curdir) + ">"

    def complete_cd(self, text, line, begidx, endidx):
        return [filename for filename in os.listdir('.') if filename.startswith(text)]

    def do_exit(self, line):
        # print(self.history)
        # input("Press a key ...")
        os.kill(os.getppid(), signal.SIGTERM)  # maybe required only with pipenv?
        return True


if __name__ == '__main__':
    shell = None
    if len(sys.argv) > 1:
        shell = Shell()
        shell.cmdloop()
    else:
        os.system("start cmd /k python " + __file__ + " new")

    if shell:
        shell.stdin = "dir\n"
        shell.stdout = "dir\n"
