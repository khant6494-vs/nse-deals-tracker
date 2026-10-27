import mysql from "mysql2/promise";
import process from "node:process";
import 'dotenv/config';

// Shared MySQL connection pool. Credentials come from .env (see DATABASE_GUIDE.md);
// defaults match docker-compose.yml.
const pool = mysql.createPool({
  host:     process.env.DB_HOST     || "127.0.0.1",
  port:     Number(process.env.DB_PORT || 3306),
  user:     process.env.DB_USER     || "nse_user",
  password: process.env.DB_PASSWORD || "nse_pass",
  database: process.env.DB_NAME     || "nse_deals",
  // server.js expects deal_date as a 'YYYY-MM-DD' string, not a JS Date
  dateStrings: true,
  connectionLimit: 10,
});

export default pool;
