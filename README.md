<img src="./img/logo.png"> <br>
# Pincode Door Lock

Members: Kenan Maslan, Nour Mazoukh, Ludvig Svensson, Moayad Saleh <br>
Program: Computer Science <br>
Course: Introducing project (1DT308) <br>
Date of submission: <br>

Presentation Video: https://www.youtube.com/watch?v=10LhsbcqLpc

## Abstract

This project aimed to create a code lock that can be controlled online through mqtt / wifi. The code lock has a 4 segment display that shows - - - - when entering numbers, it shows ```*ERROR*``` when you enter the wrong code, it shows ```*WELL*``` (for welcome) when entering the correct code.
It also shows ```*ERR*``` If something goes wrong (that the lock, for example, crashes) so that you can get the lock fixed. Key is ALWAYS an option. Because we did not have time to design a lock, we demonstrate the prototype by showing that it works when it shows ```*WELL*``` / ```*ERR*```

We have changed our mind and opted for LCD display, because its bigger, and uses less pins..

Each Error Code and the correct code must be published on a mqtt server. The purpose of this is that we will have an app called mqtt client for android / iphone, which can communicate with the lock.

We will also implement a http version of this. Both versions will be available, since we cant decide which one is better..

A temporary code can be given via the app that is either onetime use, or a code that expires after a certain time. The purpose of this is to be able to give guests the "key" but not give them the master code, because the master code is the one the owner remembers and that works forever. 
##### Through mqtt you are able to (Private Use):

See all attempts <br>
Enter a guest code <br>
Change the Master Code (in case you forget it). <br>

##### Through http you are able to (Business Use):

See all attempts <br>
Create unique users that have their own password for login <br>
Master code, along with other codes, are instead changed on an hourly basis automatically, this is a solution that makes the lock way more secure, which is the aim for most business applications. <br>

## Background and idea
Kenan had the idea to create a passcode lock, and the reason to choose this was to introduce a fun and challenging project, since it revolves around hardware, software but also servers and connections. One important focus we had is security, since the lock needs to securely lock a door. It also needs to be convenient to use, so to find the balance between security and confort. Our hopes is to have a lock that works well, is practical, but also secure. <br>


## Method

[Hardware](/doc/hardware.md) <br>

[Requirements](/doc/requirements.md) <br>

[Server](/doc/server.md) <br>

[Setup](/doc/setup.md) <br>

[Timelog](/doc/timelog.md) <br>

[Test](/doc/Test.md) <br>

## Results
##### Finished product inside of its box (Online mode, no offline displayed):

<img src="/img/IMG_0801.jpg" width="400"> <br>

##### Example of device displaying cooldown (Due to too many attempts):

<img src="/img/6A2AAF88-0D64-4F93-8833-04A7A3DEE566.jpeg" width="400"> <br>

##### Example of device displaying OFFLINE mode:

<img src="/img/7BF9CD29-DAF8-4D78-B619-2D273664678F.jpeg" width="400"> <br>

##### Successful Passcode Input:

<img src="/img/968BBDDE-E100-49DA-B5A1-F882539DFB42.jpeg" width="400"> <br>

##### Connection Screen (To Wifi):

<img src="/img/F6CCDCB9-5C20-4A62-BCBA-D63CB1D1ACB2.jpeg" width="400"> <br>

##### Screen with some digits inputted (Also, in offline state):

<img src="/img/image.jpg" width="400"> <br>

##### Example of editing device on website (pinlock.nor.nu):

<img src="/img/ui/device-edit.png" width="400"> <br>

##### The logic flow:
<img src="/img/flow.png" width="400"> <br>


