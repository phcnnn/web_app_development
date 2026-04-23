# 快速小資記帳 (QuickSpend) — 路由設計文件

> 本文件定義了系統的 URL 路徑、HTTP 方法與前後端互動邏輯，為開發實作提供標準依據。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與統計** | `GET` | `/` | `index.html` | 顯示當月總支出統計與所有消費紀錄清單 |
| **新增消費** | `POST` | `/add` | — | 接收表單資料，建立新紀錄後重導向至首頁 |
| **編輯頁面** | `GET` | `/edit/<int:id>` | `edit.html` | 顯示特定紀錄的編輯表單（預填現有資料） |
| **更新消費** | `POST` | `/edit/<int:id>` | — | 接收修改後的資料，更新 DB 後重導向至首頁 |
| **刪除消費** | `POST` | `/delete/<int:id>` | — | 刪除指定 ID 的紀錄後重導向至首頁 |

---

## 2. 路由詳細說明

### 2.1 首頁 (GET `/`)
- **輸入**：無。
- **處理邏輯**：
    1. 呼叫 `Transaction.get_all()` 取得所有紀錄。
    2. 呼叫 `Transaction.get_total_spending()` 計算當月總支出。
- **輸出**：渲染 `index.html`，傳入 `records` 與 `total_amount`。
- **錯誤處理**：若資料庫讀取失敗，顯示 500 錯誤頁面。

### 2.2 新增消費 (POST `/add`)
- **輸入**：表單欄位 `amount` (float), `category` (string), `memo` (string)。
- **處理邏輯**：
    1. 驗證 `amount` 與 `category` 是否為空。
    2. 呼叫 `Transaction.create(amount, category, memo)`。
- **輸出**：`redirect(url_for('index'))`。
- **錯誤處理**：資料驗證失敗時，重導向回首頁並透過 Flask Flash 顯示錯誤訊息。

### 2.3 編輯頁面 (GET `/edit/<int:id>`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `Transaction.get_by_id(id)` 取得資料。
- **輸出**：渲染 `edit.html`，傳入 `transaction` 物件。
- **錯誤處理**：若找不到該 ID，回傳 404 Not Found。

### 2.4 更新消費 (POST `/edit/<int:id>`)
- **輸入**：表單欄位 `amount`, `category`, `memo`。
- **處理邏輯**：呼叫 `Transaction.update(id, amount=..., category=..., memo=...)`。
- **輸出**：`redirect(url_for('index'))`。
- **錯誤處理**：若 ID 不存在回傳 404；驗證失敗則導回編輯頁並顯示提示。

### 2.5 刪除消費 (POST `/delete/<int:id>`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `Transaction.delete(id)`。
- **輸出**：`redirect(url_for('index'))`。
- **錯誤處理**：若刪除失敗或 ID 不存在，透過 Flash 顯示錯誤訊息。

---

## 3. Jinja2 模板清單

所有模板皆繼承自 `base.html` 以維持 UI 一致性。

| 模板檔案 | 繼承自 | 說明 |
| :--- | :--- | :--- |
| `base.html` | — | 基礎版型，包含導覽列、CSS 引入與 Flash 訊息容器 |
| `index.html` | `base.html` | 首頁：上方顯示當月統計，中央為新增表單，下方為紀錄列表 |
| `edit.html` | `base.html` | 編輯頁：單獨的編輯表單，可修改指定紀錄 |

---

## 4. 路由設計準則

- **RESTful 實踐**：雖然 HTML Form 限制使用 POST，但 URL 仍盡量保持直觀的名詞與 ID 定位。
- **PRG 模式**：所有修改資料的操作 (Add, Update, Delete) 成功後，一律使用 302 Redirect，避免使用者重新整理頁面造成重複操作。
- **Flash 提示**：使用 Flask `flash()` 提供操作成功或失敗的即時回饋。

---
*文件版本：v1.0 | 建立日期：2026-04-23*
