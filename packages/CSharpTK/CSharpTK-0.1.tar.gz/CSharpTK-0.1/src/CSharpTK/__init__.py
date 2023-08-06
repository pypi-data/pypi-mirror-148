import os
import os.path


def System(Command):
    """
    通过os.system，在控制台输出指令。

    :param Command: os.system(command)
    """
    return os.system(Command)


class DotNet(object):
    def __init__(self):
        """
        DotNet 用于连接.Net框架。如创建项目都要使用，是个十分主要的模块
        """
        self.Sln = "sln"
        self.Console = "console"
        self.Classlib = "classlib"
        self.EditorConfig = "editorconfig"
        self.NuGet = "NuGet"
        ############################################### Windows Forms
        self.WinformConstrolLib = "winformscontrollib"
        self.Winforms = "winforms"
        self.WinformsLib = "winformslib"
        ############################################### Windows WPF
        self.WpfLib = "wpflib"
        self.WpfApplication = "wpf"
        self.WpfUserControlLib = "wpfusercontrollib"
        self.WpfCustomControlLib = "wpfcustomcontrollib"

    def Info(self):
        """
        在控制台返回dotnet的资料信息。
        """
        return System("dotnet --info")

    def Pause(self):
        """
        在控制台输出pause，为需要用户输入才会进行下一步
        """
        return System("pause")

    def New(self, AppType, Force: bool = False):
        """
        创建一个新项目

        :param AppType: 为App的类型。
        :param Force:  为创建时是否覆盖已有的重名App
        """
        if Force:
            return System(f"dotnet new {AppType} --force")
        elif not Force:
            return System(f"dotnet new {AppType}")

    def NewNone(self):
        """
        在控制台输入dotnet new。
        """
        return System("dotnet new")

    def NewHelp(self):
        """
        获取DotNet New方法的帮助
        """
        return System("dotnet new --help")

    def NewInstall(self, Module: str):
        """
        在控制台输入安装模块

        :param Module:
        """
        return System(f"dotnet new --install {Module}")

    def NewUnInstall(self, Module: str):
        return System(f"dotnet new --uninstall {Module}")

    def NewType(self):
        return System("dotnet new --list")

    def Build(self):
        return System("dotnet build")

    def BuildHelp(self):
        return System("dotnet build --help")

    def MsBuild(self):
        return System("dotnet msbuild")

    def Clean(self):
        return System("dotnet clean")

    def Help(self):
        return System("dotnet help")

    def List(self):
        return System("dotnet list")

    def Run(self):
        return System("dotnet run")

    def RunHelp(self):
        return System("dotnet run --help")

    def Test(self):
        return System("dotnet test")

    def TestHelp(self):
        return System("dotnet test --help")

    def VSTest(self):
        return System("dotnet vstest --help")

    def VSTestHelp(self):
        return System("dotnet vstest --help")

    def Pack(self):
        return System("dotnet pack")

    def PackHelp(self):
        return System("dotnet pack --help")

    def GetBin(self):
        return f"{os.getcwd()}\\bin\\Debug\\net6.0-windows\\"


class DotNetSimple(DotNet):
    def CreatorConsoleApp(self, F: bool = False):
        self.New(self.Console, Force=F)

    def CreatorWindowsForms(self, F: bool = False):
        self.New(self.Winforms, Force=F)

    def CreatorWPFApplication(self, F: bool = False):
        self.New(self.WpfApplication, Force=F)

    def RunAppliction(self):
        self.Build()
        self.Run()


class File(object):
    def __init__(self, File, Mode, Close: bool = False):
        self.File = open(File, Mode)

        if Close:
            self.File.close()

    def __str__(self):
        return self.File

    def GetFileName(self):
        return self.File.name

    def GetMode(self):
        return self.File.mode

    def Clear(self):
        return self.File.write("")

    def Write(self, Strings):
        return self.File.write(Strings)

    def WriteLines(self, Strings):
        return self.File.writelines(Strings)

    def Read(self):
        return self.File.read()

    def Close(self):
        self.File.close()


class Program(object):
    def __init__(self, Custom: str = "Program.cs"):
        self.Program = File(Custom, "w")

    def GetFileName(self):
        return self.Program.GetFileName()

    def GetMode(self):
        return self.Program.GetMode()

    def Clear(self):
        self.Program.Clear()

    def ConsoleWirteLineStrings(self, String, End="\n"):
        self.Program.WriteLines(f'Console.WriteLine("{String}");{End}')

    def System(self, Command, End="\n"):
        self.Program.WriteLines(f'System("{Command}");{End}')

    def SystemPause(self, End="\n"):
        self.System(Command="pause", End=End)

    def Close(self):
        self.Program.Close()