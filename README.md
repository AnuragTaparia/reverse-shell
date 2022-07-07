## REVERSE SHELL

There are many ways to gain control over a compromised system. A common practice is to gain interactive shell access, which enables you to try to gain complete control of the operating system. However, most basic firewalls block direct remote connections. One of the methods to bypass this is to use reverse shells.

A reverse shell is a program that executes local cmd.exe (for Windows) or bash/zsh (for Unix-like) commands and sends the output to a remote machine. With a reverse shell, the target machine initiates the connection to the attacker machine, and the attacker's machine listens for incoming connections on a specified port; this will bypass firewalls.

The basic idea of the code we will implement is that the attacker's machine will keep listening for connections. Once a client (or target machine) connects, the server will send shell commands to the target machine and expect output results.

#### There are two type of reverse shell that I have made

- [Single Client](https://github.com/AnuragTaparia/reverse-shell/tree/master/single%20client)
- [Multiple Client](https://github.com/AnuragTaparia/reverse-shell/tree/master/multi%20client)
