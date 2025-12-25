# ./app/core/seed.py

from sqlmodel import Session, select
from app.core.security import get_password_hash
from app.modules.users.models import User
from app.modules.users.enums import UserRole
from app.modules.doctors.models import DoctorProfile


def seed_initial_data(session: Session):
    """Create initial users if they don't exist"""
    
    # Check if we already have users
    existing_users = session.exec(select(User)).first()
    if existing_users:
        print("Database already has users, skipping seed...")
        return
    
    print("Seeding initial data...")
    
    hashed_password = get_password_hash("secret")
    
    # 1. Create Sysadmin (Superuser)
    sysadmin = User(
        email="sysadmin@example.com",
        full_name="System Administrator",
        hashed_password=hashed_password,
        role=UserRole.SYSADMIN,
        telegram_username="@sysadmin"
    )
    session.add(sysadmin)
    session.flush()  # Get ID before creating profile
    
    # Sysadmin also gets doctor profile (can take shifts)
    sysadmin_profile = DoctorProfile(
        user_id=sysadmin.id,
        priority=1,
        min_shifts_per_month=0
    )
    session.add(sysadmin_profile)
    
    # 2. Create Admin
    admin = User(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password=hashed_password,
        role=UserRole.ADMIN,
        telegram_username="@admin"
    )
    session.add(admin)
    
    # 3. Create 5 Doctors
    doctors_data = [
        {"email": "doctor1@example.com", "full_name": "Иванов Иван Иванович", "telegram": "@ivanov"},
        {"email": "doctor2@example.com", "full_name": "Петрова Мария Сергеевна", "telegram": "@petrova"},
        {"email": "doctor3@example.com", "full_name": "Сидоров Алексей Петрович", "telegram": "@sidorov"},
        {"email": "doctor4@example.com", "full_name": "Козлова Анна Викторовна", "telegram": "@kozlova"},
        {"email": "doctor5@example.com", "full_name": "Новиков Дмитрий Андреевич", "telegram": "@novikov"},
    ]
    
    for i, doc_data in enumerate(doctors_data, 1):
        doctor = User(
            email=doc_data["email"],
            full_name=doc_data["full_name"],
            hashed_password=hashed_password,
            role=UserRole.DOCTOR,
            telegram_username=doc_data["telegram"]
        )
        session.add(doctor)
        session.flush()
        
        # Create doctor profile
        profile = DoctorProfile(
            user_id=doctor.id,
            priority=i,  # Different priorities
            min_shifts_per_month=4
        )
        session.add(profile)
    
    session.commit()
    
    print("=" * 50)
    print("Initial users created:")
    print("=" * 50)
    print(f"{'Role':<12} {'Email':<25} {'Password'}")
    print("-" * 50)
    print(f"{'SYSADMIN':<12} {'sysadmin@example.com':<25} secret")
    print(f"{'ADMIN':<12} {'admin@example.com':<25} secret")
    for doc in doctors_data:
        print(f"{'DOCTOR':<12} {doc['email']:<25} secret")
    print("=" * 50)