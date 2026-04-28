from flask import Blueprint, render_template, request, redirect, url_for, flash
# 注意：此處假設 Transaction 模型已在 app.models.transaction.py 中定義
# from app.models.transaction import Transaction

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示當月統計與消費清單
    1. 取得所有消費紀錄 (Transaction.get_all())
    2. 計算當月總支出 (Transaction.get_monthly_total())
    3. 渲染 index.html
    """
    return render_template('index.html')

@main_bp.route('/add', methods=['POST'])
def add_transaction():
    """
    新增消費紀錄
    1. 從 request.form 取得 amount, category, memo
    2. 驗證資料合法性
    3. 呼叫 Transaction.create() 存入資料庫
    4. 重導向至首頁
    """
    # 邏輯實作將在後續階段完成
    return redirect(url_for('main.index'))

@main_bp.route('/transactions/<int:transaction_id>/edit', methods=['GET'])
def edit_page(transaction_id):
    """
    顯示編輯頁面
    1. 根據 ID 取得紀錄 (Transaction.get_by_id())
    2. 渲染 edit.html 並帶入紀錄資料
    """
    return render_template('edit.html')

@main_bp.route('/transactions/<int:transaction_id>/update', methods=['POST'])
def update_transaction(transaction_id):
    """
    更新消費紀錄
    1. 從 request.form 取得更新後的 amount, category, memo
    2. 呼叫 Transaction.update() 更新資料
    3. 重導向至首頁
    """
    return redirect(url_for('main.index'))

@main_bp.route('/transactions/<int:transaction_id>/delete', methods=['POST'])
def delete_transaction(transaction_id):
    """
    刪除消費紀錄
    1. 呼叫 Transaction.delete() 刪除指定紀錄
    2. 重導向至首頁
    """
    return redirect(url_for('main.index'))
