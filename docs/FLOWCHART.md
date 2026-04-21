# 食譜收藏夾系統 — 流程圖文件

> 根據 `docs/PRD.md` 與 `docs/ARCHITECTURE.md` 設計，涵蓋使用者操作流程與系統資料流。

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁：食譜列表]

    B --> C{要執行什麼操作？}

    C -->|瀏覽食譜| D[查看食譜詳細頁]
    D --> E{繼續操作？}
    E -->|編輯| F[填寫編輯表單]
    F --> F1[送出表單]
    F1 --> D
    E -->|刪除| G{確認刪除？}
    G -->|確認| H[刪除食譜]
    H --> B
    G -->|取消| D

    C -->|新增食譜| I[填寫新增表單]
    I --> I1[輸入：名稱 / 簡介 / 時間 / 分類]
    I1 --> I2[新增食材清單]
    I2 --> I3[新增製作步驟]
    I3 --> I4[送出表單]
    I4 --> D

    C -->|搜尋食譜| J[輸入關鍵字]
    J --> K[搜尋結果頁]
    K -->|點選食譜| D
    K -->|重新搜尋| J

    C -->|根據食材推薦| L[輸入手邊食材]
    L --> M[系統篩選符合食譜]
    M --> N[推薦結果頁]
    N -->|點選食譜| D
    N -->|重新輸入| L

    C -->|依分類篩選| O[選擇分類]
    O --> P[篩選後的食譜列表]
    P -->|點選食譜| D
    P -->|返回| B
```

---

## 2. 系統序列圖（System Sequence Diagram）

描述各主要功能在系統內部的完整資料流，角色包含：使用者、Flask Route（Controller）、SQLAlchemy Model、SQLite 資料庫。

---

### 2.1 查看食譜列表（GET /）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Flask: GET /（開啟首頁）
    Flask->>Model: Recipe.query.all()
    Model->>DB: SELECT * FROM recipe
    DB-->>Model: 回傳所有食譜資料列
    Model-->>Flask: 回傳 Recipe 物件清單
    Flask-->>User: render_template('index.html', recipes=...)
```

---

### 2.2 新增食譜（POST /recipe/create）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Flask as Flask Route
    participant Model as Recipe / Ingredient Model
    participant DB as SQLite

    User->>Flask: GET /recipe/create（開啟新增表單）
    Flask-->>User: render_template('recipe/create.html')

    User->>Flask: POST /recipe/create（填寫表單送出）
    Flask->>Flask: 驗證表單資料（必填欄位、格式檢查）

    alt 驗證失敗
        Flask-->>User: 重新顯示表單，附帶錯誤提示
    else 驗證成功
        Flask->>Model: 建立 Recipe 物件
        Flask->>Model: 建立 Ingredient 物件（多筆）
        Model->>DB: INSERT INTO recipe
        Model->>DB: INSERT INTO ingredient（多筆）
        Model->>DB: INSERT INTO recipe_ingredient（關聯）
        DB-->>Model: 成功
        Model-->>Flask: 回傳新食譜 id
        Flask-->>User: redirect → /recipe/<id>（食譜詳細頁）
    end
```

---

### 2.3 查看食譜詳細內容（GET /recipe/\<id\>）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Flask: GET /recipe/<id>
    Flask->>Model: Recipe.query.get(id)
    Model->>DB: SELECT * FROM recipe WHERE id=?
    Model->>DB: SELECT * FROM ingredient JOIN recipe_ingredient WHERE recipe_id=?
    DB-->>Model: 回傳食譜 + 食材清單
    Model-->>Flask: 回傳 Recipe 物件（含關聯食材與步驟）
    Flask-->>User: render_template('recipe/detail.html', recipe=...)
```

---

### 2.4 編輯食譜（POST /recipe/\<id\>/edit）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Flask: GET /recipe/<id>/edit（開啟編輯表單）
    Flask->>Model: Recipe.query.get(id)
    Model->>DB: SELECT * FROM recipe WHERE id=?
    DB-->>Model: 回傳現有資料
    Flask-->>User: render_template('recipe/edit.html', recipe=...)

    User->>Flask: POST /recipe/<id>/edit（修改內容送出）
    Flask->>Flask: 驗證表單資料
    Flask->>Model: 更新 Recipe 欄位
    Model->>DB: UPDATE recipe SET ... WHERE id=?
    Model->>DB: 刪除舊食材 / 插入新食材
    DB-->>Model: 成功
    Flask-->>User: redirect → /recipe/<id>
```

---

### 2.5 刪除食譜（POST /recipe/\<id\>/delete）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Flask: POST /recipe/<id>/delete（點擊刪除按鈕）
    Flask->>Model: Recipe.query.get(id)
    Model->>DB: DELETE FROM recipe_ingredient WHERE recipe_id=?
    Model->>DB: DELETE FROM recipe WHERE id=?
    DB-->>Model: 成功
    Flask-->>User: redirect → /（回到首頁）
```

---

### 2.6 搜尋食譜（GET /search）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Flask as Flask Route
    participant Model as Recipe / Ingredient Model
    participant DB as SQLite

    User->>Flask: GET /search?q=關鍵字
    Flask->>Model: Recipe.query.filter( name.contains(q) OR ingredient.name.contains(q) )
    Model->>DB: SELECT DISTINCT recipe.* FROM recipe LEFT JOIN ... WHERE name LIKE ?
    DB-->>Model: 回傳符合的食譜清單
    Model-->>Flask: 回傳 Recipe 物件清單
    Flask-->>User: render_template('search/results.html', results=..., query=q)
```

---

### 2.7 根據食材推薦食譜（GET /search/by-ingredients）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Flask as Flask Route
    participant Model as Recipe / Ingredient Model
    participant DB as SQLite

    User->>Flask: GET /search/by-ingredients?ingredients=蛋,番茄
    Flask->>Flask: 解析輸入的食材清單（split by ',' ）
    Flask->>Model: 對每個食材進行交集查詢
    Model->>DB: SELECT recipe_id FROM recipe_ingredient JOIN ingredient ON ... WHERE name IN (...)
    Model->>DB: GROUP BY recipe_id HAVING COUNT(DISTINCT ingredient_id) = 食材數量
    DB-->>Model: 回傳完整符合的食譜 id 清單
    Model-->>Flask: 查詢並回傳 Recipe 物件清單
    Flask-->>User: render_template('search/results.html', results=..., mode='ingredients')
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 食譜列表（首頁） | `/` | GET | `index.html` | 顯示所有食譜，可依分類篩選 |
| 新增食譜（表單頁） | `/recipe/create` | GET | `recipe/create.html` | 顯示新增食譜的空白表單 |
| 新增食譜（送出） | `/recipe/create` | POST | — | 處理表單，建立食譜後導回詳細頁 |
| 食譜詳細內容 | `/recipe/<id>` | GET | `recipe/detail.html` | 顯示食譜基本資訊、食材、步驟 |
| 編輯食譜（表單頁） | `/recipe/<id>/edit` | GET | `recipe/edit.html` | 顯示預填現有資料的編輯表單 |
| 編輯食譜（送出） | `/recipe/<id>/edit` | POST | — | 更新食譜資料後導回詳細頁 |
| 刪除食譜 | `/recipe/<id>/delete` | POST | — | 刪除食譜與關聯食材後導回首頁 |
| 關鍵字搜尋 | `/search` | GET | `search/results.html` | 依名稱或食材關鍵字搜尋食譜 |
| 食材推薦 | `/search/by-ingredients` | GET | `search/results.html` | 依多項食材交集查詢推薦食譜 |

---

*文件版本：v1.0 | 建立日期：2026-04-21 | 對應架構文件：ARCHITECTURE.md v1.0*
