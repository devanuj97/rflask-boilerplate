# Boilerplate - FRM

Boilerplate project for Flask, React & MongoDB based projects. This README documents the steps necessary to get your
application up and running.

## Table of Contents

- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Integrations](#integrations)
- [Deployment](#deployment)

## Getting Started

**Quickstart:**

- This project supports running the application with all the required dependencies using `docker compose`.
- Install [docker](https://docs.docker.com/engine/install/).
- Run `docker compose -f docker-compose.dev.yml up` (Add `--build` to force rebuild when new dependencies have been
  added).
- The application should open up automatically. If it doesn't, go to `http://localhost:3000`.
- Make required changes for development. Both backend and frontend should hot reload, and server restart is not
  required.

**Bonus:**

- On running `serve`, the frontend server is at `http://localhost:3000`.
- On running `serve`, the backend server is at `http://localhost:8080`.
- To connect to MongoDB server using a client, use `mongodb://localhost:27017`.

**Pre Requirements:**

- Python (v3.11)
- Node (v22.13.1) - [Download](https://nodejs.org/download/release/v22.13.1/)
- MongoDB (v5) - [Download](https://www.mongodb.com/docs/manual/installation/)

**Scripts:**

- Install dependencies - `npm install`
- Install Python dependencies - `pipenv install --dev`
- Build Project - `npm build`
- Start Application (without HotReload) - `npm start`
- Start Application (with HotReload enabled) - `npm run serve`
  - To disable opening up the browser automatically, set `WEBPACK_DEV_DISABLE_OPEN` to `true`.
- Lint Check - `npm run lint`
- Format Code - `npm run fmt`

## Configuration

In the `src/apps/backend/settings/` directory:

We are keeping config as a schema environment specific.

Example:

- For development - we have `development.py` and so for other environments.

Based on the environment which will be passed during spawning the server as an argument
with `APP_ENV=<environment_name>`, this will further load the schema accordingly.

Note:

- `default.py` - This file will be used to keep all our **constant values**.
- If no environment name is passed, the default environment will be considered as `development`.

**.env File**

Application also supports loading environment variables from `.env` file. Just add the file to `src/apps/backend` and it
should be picked up by the server.

**UI Config:**

In case of need of config values at client-side, this will make an internal request to the backend server to get the
desired config schema in the form of JSON.

## Scripts

This application also supports running one off scripts. Helpful during development or running cron jobs.

Steps:

- Create a python file under - `src/apps/backend/scripts` (ex - `my-script.py`)
- Run the script using npm - `npm run script --file=example_worker_script`

## Deployment

This project deploys on Kubernetes via GitHub actions using workflows defined
in [GitHub CI](https://github.com/jalantechnologies/github-ci).
