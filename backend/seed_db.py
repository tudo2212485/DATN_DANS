import os
import sys

# Ensure the app module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.models import Base, User
from app.core.security import get_password_hash

def seed_users():
    # Create tables if not exist
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    try:
        users_to_seed = [
            {
                "email": "admin@agroforecast.vn",
                "full_name": "Quản trị viên Hệ thống",
                "password": "admin123",
                "role": "admin"
            },
            {
                "email": "anhnguyen@agroforecast.vn",
                "full_name": "Nguyễn Văn Ánh (Analyst)",
                "password": "123456",
                "role": "analyst"
            }
        ]
        
        for u in users_to_seed:
            existing = db.query(User).filter(User.email == u["email"]).first()
            if not existing:
                new_user = User(
                    email=u["email"],
                    full_name=u["full_name"],
                    password_hash=get_password_hash(u["password"]),
                    role=u["role"]
                )
                db.add(new_user)
                print(f"Created user: {u['email']}")
            else:
                existing.password_hash = get_password_hash(u["password"])
                print(f"Updated password for: {u['email']}")
                
        db.commit()
        print("Database seeding completed.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
