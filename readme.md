# Python Weather Project
## About
This is a simple project that I made to try out FastAPI with React front-end. Essentially, it fetches weather data from WeatherAPI and sends it to the connected MongoDB collection. 

It also allows the user to use all the nice little CRUD-operations that they would expect.

The project began as a simple CLI-based weather app that accomplished largely the same things, but upon seeing Eric Roby's tutorial on React + FastAPI, I decided to try my hand at it.
You can find the tutorial [here](https://youtu.be/0zb2kohYZIM). 

The keen-eyed among you will no doubt notice that the UI looks near identical. This is on purpose. It achieves what it sets out to do, and I am more interested in backend development.

Also, if you wish, you can also find the old CLI-based files in the "Old Files" directory.
## Status
Finished. Pay no attention to the quality of the front-end, for it is mostly held together by faith and luck.

## Technologies
- FastAPI
- MongoDB
- React
- Bootstrap
- Axios

## Installation

Prerequisites
- Python 3.10+ (or newer)
- Node.js 18+ and npm (for the React front-end)
- MongoDB (local or Atlas) and a WeatherAPI account/key

Backend (FastAPI)
1. From the project root create and activate a virtual environment:

   python3 -m venv .venv
   source .venv/bin/activate

2. Install Python dependencies:

   pip install -r requirements.txt

3. Create a .env file in the project root with the following values (example):

   API_KEY=your_weatherapi_key_here
   MONGODB_URL=

4. Start the FastAPI server:

   uvicorn FastAPI.main:app --reload --host 0.0.0.0 --port 8000

Frontend (React)
1. Change to the front-end directory:

   cd React/front-end

2. Install Node dependencies and start the dev server:

   npm install
   npm start

The React app runs at http://localhost:3000 and is configured to talk to the API at http://localhost:8000 (see React/front-end/src/api.js).

Building for production
- Front-end: from React/front-end run npm run build and serve the build/ directory with any static server.

Notes
- Use an appropriate MONGODB_URL for Atlas (include user/password) or a local MongoDB URI.
- Keep your API_KEY and DB credentials secret; do not commit .env to version control.
 - If ports conflict, change the uvicorn --port and update React/front-end/src/api.js accordingly.


## Regarding AI-/LLM-usage
JetBrains Junie chat was utilised, especially with React, alongside auto-completions where it did not break anything. In the later stages of the project I decided to try out Junie's agent-mode, allowing it to add and modify parts of the project. It worked adequately enough.

GitHub Copilot also wrote the installation instructions.