from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.transaction import Transaction

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示當月統計與消費清單
    """
    transactions = Transaction.get_all()
    total_spending = Transaction.get_monthly_total()
    return render_template('index.html', transactions=transactions, total_spending=total_spending)

@main_bp.route('/add', methods=['POST'])
def add_transaction():
    """
    新增消費紀錄
    """
    try:
        amount_str = request.form.get('amount')
        category = request.form.get('category')
        memo = request.form.get('memo')

        # 基本驗證
        if not amount_str or not category:
            flash("金額與類別為必填欄位！", "error")
            return redirect(url_for('main.index'))
        
        amount = float(amount_str)
        if amount <= 0:
            flash("金額必須大於 0！", "error")
            return redirect(url_for('main.index'))

        # 呼叫 Model 建立紀錄
        success = Transaction.create(amount, category, memo)
        if success:
            flash("新增成功！", "success")
        else:
            flash("新增失敗，請稍後再試。", "error")
            
    except ValueError:
        flash("請輸入正確的金額格式！", "error")
    except Exception as e:
        flash(f"發生非預期錯誤：{e}", "error")

    return redirect(url_for('main.index'))

@main_bp.route('/transactions/<int:transaction_id>/edit', methods=['GET'])
def edit_page(transaction_id):
    """
    顯示編輯頁面
    """
    transaction = Transaction.get_by_id(transaction_id)
    if not transaction:
        flash("找不到該筆紀錄！", "error")
        return redirect(url_for('main.index'))
    
    return render_template('edit.html', transaction=transaction)

@main_bp.route('/transactions/<int:transaction_id>/update', methods=['POST'])
def update_transaction(transaction_id):
    """
    更新消費紀錄
    """
    try:
        amount_str = request.form.get('amount')
        category = request.form.get('category')
        memo = request.form.get('memo')

        if not amount_str or not category:
            flash("金額與類別為必填欄位！", "error")
            return redirect(url_for('main.edit_page', transaction_id=transaction_id))

        data = {
            'amount': float(amount_str),
            'category': category,
            'memo': memo
        }

        success = Transaction.update(transaction_id, data)
        if success:
            flash("更新成功！", "success")
            return redirect(url_for('main.index'))
        else:
            flash("更新失敗！", "error")
            
    except ValueError:
        flash("請輸入正確的金額格式！", "error")
    
    return redirect(url_for('main.edit_page', transaction_id=transaction_id))

@main_bp.route('/transactions/<int:transaction_id>/delete', methods=['POST'])
def delete_transaction(transaction_id):
    """
    刪除消費紀錄
    """
    success = Transaction.delete(transaction_id)
    if success:
        flash("紀錄已刪除！", "success")
    else:
        flash("刪除失敗！", "error")
        
    return redirect(url_for('main.index'))
