from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    memo = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.id}: {self.category} ${self.amount}>'

    def to_dict(self):
        """將物件轉換為字典格式，方便 API 使用"""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'memo': self.memo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def create(amount, category, memo=None):
        """新增一筆消費紀錄"""
        try:
            new_transaction = Transaction(
                amount=amount,
                category=category,
                memo=memo
            )
            db.session.add(new_transaction)
            db.session.commit()
            return new_transaction
        except Exception as e:
            db.session.rollback()
            print(f"Error creating transaction: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有消費紀錄，按時間倒序排序"""
        try:
            return Transaction.query.order_by(Transaction.created_at.desc()).all()
        except Exception as e:
            print(f"Error fetching all transactions: {e}")
            return []

    @staticmethod
    def get_by_id(transaction_id):
        """取得單筆消費紀錄"""
        try:
            return Transaction.query.get(transaction_id)
        except Exception as e:
            print(f"Error fetching transaction {transaction_id}: {e}")
            return None

    @staticmethod
    def update(transaction_id, data):
        """更新消費紀錄"""
        try:
            transaction = Transaction.query.get(transaction_id)
            if transaction:
                transaction.amount = data.get('amount', transaction.amount)
                transaction.category = data.get('category', transaction.category)
                transaction.memo = data.get('memo', transaction.memo)
                db.session.commit()
                return transaction
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error updating transaction {transaction_id}: {e}")
            return None

    @staticmethod
    def delete(transaction_id):
        """刪除消費紀錄"""
        try:
            transaction = Transaction.query.get(transaction_id)
            if transaction:
                db.session.delete(transaction)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting transaction {transaction_id}: {e}")
            return False

    @staticmethod
    def get_monthly_total():
        """計算當月總支出 (輔助方法，非 skill 硬性要求但 PRD 需要)"""
        try:
            now = datetime.utcnow()
            # 簡單過濾當月 (實務上應考慮跨年)
            current_month_transactions = Transaction.query.filter(
                db.extract('month', Transaction.created_at) == now.month,
                db.extract('year', Transaction.created_at) == now.year
            ).all()
            return sum(t.amount for t in current_month_transactions)
        except Exception as e:
            print(f"Error calculating monthly total: {e}")
            return 0
