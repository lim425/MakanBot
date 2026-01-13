# MakanBot
### Voice & Head Gesture Controlled Assistive Feeding Robot

## Project Overview

MakanBot is an assistive robotic feeding system designed to help individuals with limited upper-limb mobility to eat independently.  The system allows users to select and pick up food using voice commands or head gestures, enabling hands-free interaction with the robotic arm.

## Demonstration

[MakanBot Demonstration Video](https://youtu.be/BbxMgMGevlQ)
![Alt Text](https://github.com/lim425/MakanBot/blob/ab7fbc7f3a6404202afc145b8a357a349071b279/docs/images/MakanBot_profile.png)

## Key Features

- Dual control modes: Voice commands and head gestures
- 4-DOF robotic arm for pick-and-feed operation
- Graphical User Interface (GUI) for system interaction
- IoT integration for remote monitoring and data logging

## System Architecture

### Hardware Components
- Laptop (main processing unit)
- 4-DOF robotic arm

### Software Components
- **OpenCV & MediaPipe** – Head gesture detection
- **Google Web Speech API** – Voice command recognition
- **PySide6** – Graphical User Interface (GUI)
- **Blynk** – IoT connectivity and monitoring

## Working Principle

-  The user selects food using voice or head gestures.
- The system processes the input on the laptop.
- Control commands are sent to the robotic arm.
- The arm performs the pick-and-feed action.
- Information logging to Blynk dashboard.

## Acknowledgements

[Build Some Stuff](https://www.youtube.com/watch?v=AIsVlgopqJc)
