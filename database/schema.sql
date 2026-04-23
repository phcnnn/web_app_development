-- 快速小資記帳 (QuickSpend) 資料庫架構
-- 建立日期：2026-04-23

-- 1. 消費紀錄表
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,           -- 消費金額
    category TEXT NOT NULL,         -- 消費類別 (餐飲, 交通, 購物, 其他)
    memo TEXT,                      -- 備忘內容
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP -- 紀錄時間
);
