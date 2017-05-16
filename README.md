# securityCamera
Final Project for UConn CSE 4709 - Networked Embedded Architecture

A crude Raspberry Pi based security camera that captures and sends images via SMTP and MMS based upon light sensitivity.
Inspired by MotionPie, found here: https://github.com/ccrisan/motionpie

Materials

    Raspberry Pi 3 Model B
    Raspberry Pi Camera Module
    SG09 servomotor
    Two 0.47 microFarad capacitors
    Photoresistor
    2.2 kiloOhm resistor
    Breadboard

![Alt text](/Breadboad_diagram.png?raw=true "Breadboard Diagram")

Breadboard is an RC (Resistor-Capacitor) circuit.

The photoresistor on the breadboard detects light and activates the camera, which takes pictures at 30°, 90°, and 120°.

It is best placed in a corner of the room for maximal coverage, but range of motion can be altered. 

Formal writeup with data TBD.
