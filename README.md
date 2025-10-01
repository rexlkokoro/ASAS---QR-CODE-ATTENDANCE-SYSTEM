QR-Code Attendance System

A modern attendance-tracking application that combines QR code scanning and facial recognition to verify and log attendees automatically. Built with Python 3, OpenCV, PyZbar, Pillow and MySQL (running in Docker).

Overview

Instead of a paper sign-in sheet, each participant receives a unique QR code generated during registration. At check-in time, the app uses a webcam to:

Scan the attendee’s QR code (“something you have”).

Match the attendee’s live face against the stored photo (“something you are”).

Only when both factors match does the system confirm attendance and record it in the database.

How it works

User registration is done through a simple form. User details and a face photo are stored in the database, and a QR code is generated for each user.

At check-in, the webcam feed is analysed in real time. The app decodes the QR code, looks up the attendee’s details and prepares a temporary recogniser model.

Facial recognition runs on the live camera feed to ensure the person holding the QR code matches the stored photo.

Attendance logging: if verification succeeds, the app inserts an entry with user ID and timestamp into the MySQL attendance table.

Cleanup: the temporary recogniser data created for that check-in is removed automatically.

Security

This system enforces a basic form of multi-factor authentication:

Something you have: your event QR code.

Something you are: your face detected by OpenCV.

This makes it much harder for someone else to register attendance on your behalf.

Tech Stack

Python 3 (OpenCV, PyZbar, Pillow, mysqlclient)

MySQL 5.7 running in a Docker container (schema initialised automatically)

Docker Compose orchestration for quick setup

Works on Windows (app runs locally) or Linux (with camera support)
