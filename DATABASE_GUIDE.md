# NSE Deals Tracker - Database Setup Guide

This document outlines how to start and manage the MySQL database backing the NSE Deals Tracker application.

## Prerequisites
- **Docker** and **Docker Compose** must be installed on your machine.
- Ports `3306` (MySQL) must be available.

## Starting the Database

The database is fully containerized. To spin it up, simply run:
```bash
docker-compose up -d
```
This will start the `nse-mysql` container in the background.

## Database Initialization
- **Schema**: On first start, `docker-compose.yml` mounts `db/schema.sql` into the container's init directory, which creates the `deals` table automatically.
- **Seeding**: Load the bundled dataset with `python db/seed_from_json.py`. It uses `INSERT IGNORE`, so re-running it is safe.
- **Data Persistence**: All SQL data is stored in the `nse_mysql_data` Docker volume, so it survives container restarts. `docker compose down -v` deletes it.
- **Git Ignore**: The `.env` file is gitignored so passwords are never pushed. The `db/` folder holds only code (`pool.js`, `schema.sql`, `seed_from_json.py`) and is committed.

## Connection Credentials
The backend reads from a local `.env` file to connect to the database. Ensure your `.env` contains:
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=nse_user
DB_PASSWORD=nse_pass
DB_NAME=nse_deals
```

## Stopping the Database
To stop the database from running in the background, run:
```bash
docker-compose down
```

## Useful Commands
- **Check Logs**: `docker logs nse-mysql`
- **Access MySQL Shell**: `docker exec -it nse-mysql mysql -u nse_user -p`
