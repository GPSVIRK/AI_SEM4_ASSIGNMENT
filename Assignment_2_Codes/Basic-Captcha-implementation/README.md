# Basic-Captcha-implementation

## Description

This program implements a simplified CAPTCHA system.
A distorted word is displayed, and the user must select all semantically related distorted words from a list of three options in order to be validated as human.

## 1. Technologies Used

  * Python 3.x
  * Tkinter
  * Pillow
  * Random module

## 2. Project Structure
```
project/
│
├── main.py
├── logic.py
├── ui.py
├── images/
│   ├── apple.png
│   ├── car.png
│   ├── banana.png
│   ├── steering.png
│   ├── mango.png
│   ├── tire.png
│   ├── wheel.png
│   └── pineapple.png
└── README.md
```
## 3. How to Run

  * Install Python 3.x.

  * Install Pillow:

     - ```pip install pillow```

  * Ensure all distorted images are located inside the images/ folder.

  * Run the program:

    - ```python main.py```
## 4. How It Works

Words are pre-mapped to semantic categories.
Four words are selected randomly per round.
One word is displayed as the main distorted word.
Three distorted words are displayed as selectable options.
The selected words are validated against the semantic mapping.
The user passes only if all and only the correct related words are selected.

## 5. Design Decisions

  * Pre-generated distorted images were used instead of dynamic distortion to reduce implementation complexity and focus on semantic validation.

  * Semantic relationships are manually defined rather than dynamically computed.

  * Tkinter was chosen for its simplicity and built-in GUI support in Python.

## 6. Limitations

Only two semantic categories are implemented.
The dataset of words is limited.
No dynamic semantic similarity or NLP-based validation is used.
