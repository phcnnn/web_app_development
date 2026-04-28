from app import create_app, db
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 確保 instance 資料夾存在（SQLite 需要）
        if not os.path.exists('instance'):
            os.makedirs('instance')
        db.create_all()
        print("Database initialized!")
    
    app.run(debug=True)
