# Freek Golf

Freek Golf is a small Flask web app for starting a casual golf round and tracking players' scores on the fly. The project is currently a lightweight prototype with a simple multi-page flow for selecting a course, choosing players, and viewing the live round screen.

## What the app does

The app lets a user:

- open the home screen and begin a round
- choose a course from the available options
- select players for the current round
- view the round screen and adjust player scores with simple plus/minus controls

## Project structure

- backend/main.py: Flask app entry point and route definitions
- backend/templates/: HTML templates for each page in the app
- requirements.txt: Python dependencies for the project

## Main flow

1. The home page displays a "Start Round" button.
2. The course selection page shows available courses.
3. The player selection page lets the user choose players for the round.
4. The round page renders the selected players and allows score changes.

## Requirements

The app uses Flask and a few supporting packages. Install them with:

```bash
pip install -r requirements.txt
```

## Run the app

From the project root, run:

```bash
python backend/main.py
```

Then open the app in your browser at:

```text
http://127.0.0.1:5000/
```

## Notes

- The current implementation stores the selected players in memory while the app is running.
- The app is a prototype and uses simple static templates plus basic JavaScript for score interaction.
