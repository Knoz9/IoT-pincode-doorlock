A description on how to test the project. Write a short descriptive text on how to run each of the features 

First you connect everything as it says in [hardware.md](https://gitlab.lnu.se/1dt308/student/grupp-14---pincode-door-lock/project/-/blob/main/doc/hardware.md "LOC")

Then to be able to test everything works, you have to follow [setup.md](https://gitlab.lnu.se/1dt308/student/grupp-14---pincode-door-lock/project/-/blob/main/doc/setup.md "LOC")

To test if it is possible to change code, send "m6666" to the mqtt server, and then the lcd should show "changing password" then 6666 should be the new code.
