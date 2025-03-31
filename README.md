# DocuSecure

![diagram](docs/assets/DocuSecure.jpg)

## Table of Content

<!--toc:start-->

- [Links](#links)
- [Getting It Started](#getting-it-started)

  - [Setup the Database](#setup-the-database)
  - [Minimal Setup](#minimal-setup)
  - [With EFK](#with-efk)
  - [With Reverse Proxy](#with-reverse-proxy)
  - [With Every Thing](#with-every-thing)

  <!--toc:end-->

## Links

- **[Requirements](docs/TASK.md)**
- **[Case Study](docs/CASE_STUDY.md)**

## Getting It Started

First you'll need to clone the repository

```bash
git clone git@github.com:omareloui/DocuSecure
```

Setup envvariables

```bash
cp backend/.env.example backend/.env
```

And make sure to update the variables

### Setup the Database

Then, you'll need to setup the DB. We're using `sqlite3`

To do so setup python's venv by running

```bash
cd backend
python -m venv venv
source venv/bin/activate
```

Then install the requirements

```bash
pip install -r requirements
```

And migrate

```bash
python manage.py migrate
```

You're going to need to create a super user too, to give permissions to other
users

```bash
python manage.py createsuperuser
```

We'll run the project using `docker` make sure you have it installed on your
system. There are 4 ways you can run the app with; [Minimal
Setup](#minimal-setup), [With EFK](#with-efk), [With Reverse Proxy](#with-reverse-proxy), and
[With Every Thing](#with-every-thing)

### Minimal Setup

To run the minimal version of DocuSecure run

```bash
docker compose up -d
```

This will run the project with ElasticSearch.

Now go to `http://localhost:8000`.

### With EFK

To run the project with EFK stack (ElasticSearch, Filebeat, and Kibana) run

```bash
docker compose --profile efk up -d
```

Go to `http://localhost:8000` for the site and go to `http://localhost:5601`
for Kibana's dashboard.

### With Reverse Proxy

```bash
docker compose --profile caddy up -d
```

This will make the app available at `http://localhost`.

### With Every Thing

If you want to run the application with the reverse proxy and the EFK stack, run

```bash
docker compose --profile all -d
```
