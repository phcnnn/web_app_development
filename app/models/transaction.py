from datetime import datetime
# 注意：此處假設 db 已在 app/__init__.py 中定義
# 實作時需確保 flask_sqlalchemy 已正確初始化
from app import db

class Transaction(db.Model):
    """消費紀錄模型"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    memo = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.id}: {self.amount}>'

    # --- CRUD 方法 ---

    @classmethod
    def create(cls, amount, category, memo=None):
        """新增一筆消費紀錄"""
        new_record = cls(amount=amount, category=category, memo=memo)
        db.session.add(new_record)
        db.session.commit()
        return new_record

    @classmethod
    def get_all(cls):
        """取得所有消費紀錄，依時間降序排列"""
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, transaction_id):
        """根據 ID 取得單一紀錄"""
        return cls.query.get(transaction_id)

    @classmethod
    def update(cls, transaction_id, **kwargs):
        """更新紀錄內容"""
        record = cls.query.get(transaction_id)
        if record:
            for key, value in kwargs.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            db.session.commit()
        return record

    @classmethod
    def delete(cls, transaction_id):
        """刪除單一紀錄"""
        record = cls.query.get(transaction_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_total_spending(cls, year=None, month=None):
        """
        計算指定月份的總支出
        若未提供年月，則預設為當前月份
        """
        now = datetime.utcnow()
        year = year or now.year
        month = month or now.month
        
        # 這裡簡化處理，實際建議使用更精確的日期範圍查詢
        records = cls.query.all()
        total = sum(r.amount for r in records if r.created_at.year == year and r.created_at.month == month)
        return total
