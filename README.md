# NSE Deals Tracker

A powerful, full-stack React and Node.js application for tracking, analyzing, and visualizing Bulk and Block deals on the National Stock Exchange (NSE). 

The tracker provides deep transparency into institutional trading behavior, breaking down aggregated bulk data into actionable Insights—like the famous "Smart Money Leaderboard" and chronological "Reversal Alerts."

---

## 📸 Application Screenshots

*(**Note:** Save your screenshots to the `src/assets/` or `public/` directory and replace the placeholders below. E.g., `![Main Dashboard](./public/dashboard.png)`)*

### 1. Main Dashboard (All Deals)
![Main Dashboard Placeholder](https://via.placeholder.com/800x400.png?text=Main+Dashboard+-+All+Deals)
*Shows the completely filterable, paginated log of historic deals along with dynamically calculated "Total Buy" and "Total Sell" metrics based on live filters.*

### 2. Smart Money Leaderboard
![Leaderboard Placeholder](https://via.placeholder.com/800x400.png?text=Smart+Money+Leaderboard)
*Tracks cumulative P&L across all traded stocks for every active institutional client.*

### 3. Top 10 Profitable Clients (Expanded Constituent Trades)
![Top 10 Expanded Placeholder](https://via.placeholder.com/800x400.png?text=Top+10+Expanded+Constituent+Trades)
*Expanding a client reveals their exact mathematical pairings of block buys and sells, isolating exact holding periods and P&L percentages chronologically.*

### 4. Reversal Alerts
![Reversal Alerts Placeholder](https://via.placeholder.com/800x400.png?text=Reversal+Alerts)
*A dedicated scanner that isolates "Buy->Sell" reversals inside defined duration windows.*

---

## ✨ Core Features
- **Dynamic Filtering Engine**: Fully interconnected filters. If you search for a client on the "All Deals" table, the Top Dashboard Summary Cards recalculate the Total Value traded natively!
- **Incremental Data Merge**: Supports incremental CSV and JSON uploads by mathematically deduplicating identical trade blocks.
- **Tree-Based Data Expansion**: Dive into any aggregate client metric to see the exact sequential "Constituent Trades" that composed it.
- **LIFO/FIFO Quantity Splitting algorithms**: Automatically splits and deducts matching trade quantities between bulk blocks organically to calculate accurate P&L.
- **Dedicated Real-time Leaderboards**.

---

## 🛠️ Tech Stack
- **Frontend**: React.js, Vite, Vanilla CSS
- **Backend / API**: Express.js, Node.js
- **Database**: MySQL 8 (via Docker Compose)
- **Data Extractor**: Python (`nsepythonserver`, `mysql-connector-python`)

---

## 🚀 Setup & Installation

### Requirements
You'll need the following installed on your machine:
- [Node.js](https://nodejs.org/en/) (v20+)
- [Python 3+](https://www.python.org/downloads/) (for the seed, scraper and CSV-merge scripts)
- [Docker](https://docs.docker.com/get-docker/) with Docker Compose (for MySQL), **or** any MySQL 8 / MariaDB server you run yourself

### 1. Clone the repository
```bash
git clone https://github.com/khant6494-vs/nse-deals-tracker.git
cd nse-deals-tracker
```

### 2. Install dependencies
```bash
npm install
pip install mysql-connector-python python-dotenv nsepythonserver
```

### 3. Start MySQL
```bash
docker compose up -d
```
This starts the `nse-mysql` container with database `nse_deals` and user `nse_user` / `nse_pass`. On first start it creates the `deals` table from `db/schema.sql`.

> Using your own MySQL instead? Create the database and user, then load the schema:
> `mysql -u nse_user -p nse_deals < db/schema.sql`

### 4. Configure credentials (optional)
The app defaults to the credentials in `docker-compose.yml`. To point it elsewhere, create a `.env` file in the project root (it's gitignored):
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=nse_user
DB_PASSWORD=nse_pass
DB_NAME=nse_deals
```

### 5. Load the bundled dataset
`public/deals.json` contains about 48k bulk, block and short-sell deals (Apr 2024 – May 2026). Load them into MySQL:
```bash
python db/seed_from_json.py
```
It's safe to re-run, because duplicates are skipped. After this, use the **⟳ Refresh** button in the app to fetch newer deals from NSE, or the **Bulk CSV / Block CSV** buttons to merge NSE CSV exports.

### 6. Start the application
The `concurrently` dev script starts the Express API server on `:3001` and the Vite React server on `:5173` together.
```bash
npm run dev
```

### 7. Access the tracker
Open your browser and navigate to the local Vite URL output by the terminal.
```
http://localhost:5173
```

---

## 📁 Project Layout
| Path | Purpose |
|---|---|
| `server.js` | Express API: dashboard, leaderboard, reversal alerts, conviction scoring, client and script portfolios |
| `src/App.jsx` | React dashboard UI |
| `db/pool.js` | Shared MySQL connection pool (reads `.env`) |
| `db/schema.sql` | `deals` table definition |
| `db/seed_from_json.py` | Loads `public/deals.json` into MySQL |
| `fetch_nse_real.py` | Incremental fetch of new deals from NSE (run by **Refresh**) |
| `merge_uploaded_csv.py` | Merges an uploaded NSE CSV export into MySQL |

See [DATABASE_GUIDE.md](./DATABASE_GUIDE.md) for more on managing the database.
