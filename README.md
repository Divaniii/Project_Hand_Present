markdown
# Hand Gesture Presentation Controller

A Python application that allows you to control presentations using hand gestures, with drawing and pointer functionality.

## Features
- **Slide Navigation**: Move between slides using hand gestures
- **Pointer**: Point to specific areas on slides
- **Drawing**: Draw on slides for annotations
- **Erase**: Remove the last drawing
- **Webcam Overlay**: See yourself presenting in the corner

## Hand Gestures
- 👆 **Pointer**: Index and middle finger up `[0,1,1,0,0]`
- ✏️ **Draw**: Only index finger up `[0,1,0,0,0]`
- 🧽 **Erase**: Index, middle, and ring fingers up `[0,1,1,1,0]`
- 👈 **Previous Slide**: Only thumb up `[1,0,0,0,0]`
- 👉 **Next Slide**: Only pinky up `[0,0,0,0,1]`

## Requirements
- Python 3.8+
- OpenCV
- MediaPipe
- CVZone
- NumPy

## Installation
1. Clone this repository:
```bash
git clone https://github.com/Divaniii/Project_Hand_Present.git
Install dependencies:

bash
pip install -r requirements.txt
Add your presentation images to the Presentation/ folder

Usage
bash
python main.py
Project Structure
text
Project_Hand_Present/
├── main.py                 # Main application
├── README.md              # This file
├── requirements.txt       # Dependencies
└── Presentation/         # Folder for slide images
    ├── 1.png
    ├── 2.png
    └── ...
Controls
Move hand above the green line to activate slide navigation

Use gestures below the green line for pointer/drawing functions

Press 'q' to quit the application

Technologies Used
OpenCV for computer vision

MediaPipe for hand tracking

CVZone for gesture recognition

NumPy for coordinate mapping

text

## To close the terminal and add the README:

1. **Close the terminal** by typing `exit` or clicking the `X` on the terminal tab
2. **Create a new file** in PyCharm called `README.md`
3. **Copy and paste** the entire content above into the file
4. **Save** the file (`Ctrl + S`)

## Then run these commands in a new terminal:

```bash
git add README.md
git commit -m "Add comprehensive README with features and usage instructions"
git push origin main
