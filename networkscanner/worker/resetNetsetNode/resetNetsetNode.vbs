If Not WScript.Arguments.Named.Exists("elevate") Then
  CreateObject("Shell.Application").ShellExecute WScript.FullName _
    , """" & WScript.ScriptFullName & """ /elevate", "", "runas", 1
  WScript.Quit
End If
Set WinScriptHost = CreateObject("WScript.Shell")
Dim strPath
strPath = "cmd /c resetNetsetNode.bat"
WinScriptHost.Run strPath, 1

WScript.Sleep 5000 'Sleeps for 5 seconds