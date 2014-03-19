Description
-----------
I use mac pro, have a Windows xp in virtualbox with Bridged Adapter network.
I have a software which can only run in Windows Environment, bind 127.0.0.1:8000.
Every other softwares on Windows xp can set a proxy(127.0.0.1:8000) to connect to a secret network.

Question
-------
I want to connect to that secret network on mac pro, how should I do?

Answer
-----
I can write a program which running on Windows.
This program accept connection from mac pro, send the data to 127.0.0.1:8000,
 And accept connection from 127.0.0.1:8000, send the data to mac pro.

Problem
-------
The program use python thread, but not very efficiency.
I want to use multiprocess, gevent, nodejs, twisted, but I can not get them right.
