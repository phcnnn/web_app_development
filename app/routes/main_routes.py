from flask import Blueprint, render_template, request, redirect, url_for, flash
# 注意：此處假設 Transaction 模型已在 app/models/transaction.py 中定義
# from app.models.transaction import Transaction

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示當月統計與消費清單
    - 取得 Transaction.get_all()
    - 取得 Transaction.get_total_spending()
    - 渲染 index.html
    """
    pass

@main_bp.route('/add', methods=['POST'])
def add_transaction():
    """
    新增消費紀錄
    - 從 request.form 取得 amount, category, memo
    - 呼叫 Transaction.create()
    - 重導向至 index
    """
    pass

@main_bp.route('/edit/<int:transaction_id>', methods=['GET'])
def edit_page(transaction_id):
    """
    顯示編輯頁面
    - 呼叫 Transaction.get_by_id(transaction_id)
    - 渲染 edit.html
    """
    pass

@main_bp.route('/edit/<int:transaction_id>', methods=['POST'])
def update_transaction(transaction_id):
    """
    更新消費紀錄
    - 從 request.form 取得新資料
    - 呼叫 Transaction.update()
    - 重導向至 index
    """
    pass

@main_bp.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    """
    刪除消費紀錄
    - 呼叫 Transaction.delete()
    - 重導向至 index
    """
    pass
