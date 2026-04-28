# 快速小資記帳 (QuickSpend) — 路由設計文件

> 本文件規劃了系統的所有路由與處理邏輯，作為前後端串接的依據。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 / 紀錄清單 | GET | `/` | `index.html` | 顯示當月總支出統計與歷史消費紀錄清單 |
| 新增消費紀錄 | POST | `/add` | — | 接收金額、類別、備忘，存入資料庫後重導向至首頁 |
| 編輯頁面 | GET | `/transactions/<int:id>/edit` | `edit.html` | 顯示特定紀錄的編輯表單 |
| 更新消費紀錄 | POST | `/transactions/<int:id>/update` | — | 接收編輯後的資料，更新資料庫後重導向至首頁 |
| 刪除消費紀錄 | POST | `/transactions/<int:id>/delete` | — | 刪除指定紀錄後重導向至首頁 |

---

## 2. 路由詳細說明

### 2.1 首頁 (`/`)
- **輸入**：無。
- **處理邏輯**：
  1. 呼叫 `Transaction.get_all()` 取得所有紀錄（或按時間排序）。
  2. 呼叫 `Transaction.get_monthly_total()` 計算本月總金額。
- **輸出**：渲染 `index.html`，傳入 `transactions` 與 `total_spending`。
- **錯誤處理**：若資料庫連線失敗，顯示錯誤頁面。

### 2.2 新增紀錄 (`/add`)
- **輸入**：`amount` (FLOAT), `category` (STRING), `memo` (STRING)。
- **處理邏輯**：
  1. 驗證金額是否為正數。
  2. 呼叫 `Transaction.create(amount, category, memo)`。
- **輸出**：`redirect(url_for('main.index'))`。
- **錯誤處理**：資料驗證失敗則返回首頁並顯示 Flash 訊息。

### 2.3 編輯頁面 (`/transactions/<int:id>/edit`)
- **輸入**：`transaction_id` (URL 參數)。
- **處理邏輯**：
  1. 呼叫 `Transaction.get_by_id(transaction_id)`。
- **輸出**：渲染 `edit.html`，傳入 `transaction` 物件。
- **錯誤處理**：若 ID 不存在，回傳 404 或重導向回首頁。

### 2.4 更新紀錄 (`/transactions/<int:id>/update`)
- **輸入**：`transaction_id` (URL 參數), `amount`, `category`, `memo` (表單)。
- **處理邏輯**：
  1. 呼叫 `Transaction.update(transaction_id, data)`。
- **輸出**：`redirect(url_for('main.index'))`。
- **錯誤處理**：更新失敗則顯示 Flash 訊息。

### 2.5 刪除紀錄 (`/transactions/<int:id>/delete`)
- **輸入**：`transaction_id` (URL 參數)。
- **處理邏輯**：
  1. 呼叫 `Transaction.delete(transaction_id)`。
- **輸出**：`redirect(url_for('main.index'))`。
- **錯誤處理**：刪除失敗則顯示 Flash 訊息。

---

## 3. Jinja2 模板清單

| 檔案名稱 | 繼承模板 | 說明 |
| :--- | :--- | :--- |
| `base.html` | — | 基礎結構，包含導覽列與 CSS 連結 |
| `index.html` | `base.html` | 首頁內容：支出圓餅圖/統計、新增表單、紀錄列表 |
| `edit.html` | `base.html` | 編輯頁面：預填原資料的編輯表單 |

---

## 4. 路由骨架程式碼 (app/routes/main_routes.py)

已在 `app/routes/main_routes.py` 中建立骨架，包含：
- `index()`: 首頁顯示
- `add_transaction()`: 處理新增
- `edit_page()`: 顯示編輯頁
- `update_transaction()`: 處理更新
- `delete_transaction()`: 處理刪除

---
*文件版本：v1.0 | 建立日期：2026-04-28*
