from app.database import SessionLocal
from .models.users import User
from .models.roles import Role
from .models.books import Book
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.utils import get_password_hash  # Usamos tu función

def seed():
    db: Session = SessionLocal()
    try:
        # Crear roles si no existen
        roles_data = ["ROLE_USER", "ROLE_MODERATOR", "ROLE_ADMIN"]
        roles = []
        for name in roles_data:
            role = db.execute(select(Role).where(Role.name == name)).scalar_one_or_none()
            if not role:
                role = Role(name=name)
                db.add(role)
            roles.append(role)
        db.commit()  # Guardar roles

        # Crear usuario administrador
        admin_user = db.execute(select(User).where(User.email == "admin@example.com")).scalar_one_or_none()
        if not admin_user:
            admin_user = User(
                name="Admin",
                email="admin@example.com",
                password_hash=get_password_hash("admin123"),
                roles=[r for r in roles if r.name == "ROLE_ADMIN"]
            )
            db.add(admin_user)

        # Crear usuario moderador
        mod_user = db.execute(select(User).where(User.email == "moderator@example.com")).scalar_one_or_none()
        if not mod_user:
            mod_user = User(
                name="Moderator",
                email="moderator@example.com",
                password_hash=get_password_hash("mod123"),
                roles=[r for r in roles if r.name == "ROLE_MODERATOR"]
            )
            db.add(mod_user)
        books_data = [
            {"title": "Cien Años de Soledad", "author": "Gabriel García Márquez", "copies_available": 5},
            {"title": "Don Quijote de la Mancha", "author": "Miguel de Cervantes", "copies_available": 3},
            {"title": "1984", "author": "George Orwell", "copies_available": 7},
            {"title": "El Principito", "author": "Antoine de Saint-Exupéry", "copies_available": 10},
            {"title": "La Odisea", "author": "Homero", "copies_available": 4},
            {"title": "Hamlet", "author": "William Shakespeare", "copies_available": 6},
            {"title": "Orgullo y Prejuicio", "author": "Jane Austen", "copies_available": 8},
            {"title": "El Gran Gatsby", "author": "F. Scott Fitzgerald", "copies_available": 5},
            {"title": "Moby Dick", "author": "Herman Melville", "copies_available": 2},
            {"title": "Crimen y Castigo", "author": "Fiódor Dostoyevski", "copies_available": 3},
            {"title": "El Hobbit", "author": "J.R.R. Tolkien", "copies_available": 9},
            {"title": "La Divina Comedia", "author": "Dante Alighieri", "copies_available": 4},
            {"title": "Cumbres Borrascosas", "author": "Emily Brontë", "copies_available": 5},
            {"title": "Drácula", "author": "Bram Stoker", "copies_available": 6},
            {"title": "El Código Da Vinci", "author": "Dan Brown", "copies_available": 7},
            {"title": "El Alquimista", "author": "Paulo Coelho", "copies_available": 8},
            {"title": "El Retrato de Dorian Gray", "author": "Oscar Wilde", "copies_available": 3},
            {"title": "La Metamorfosis", "author": "Franz Kafka", "copies_available": 6},
            {"title": "Los Miserables", "author": "Victor Hugo", "copies_available": 4},
            {"title": "Fahrenheit 451", "author": "Ray Bradbury", "copies_available": 5},
        ]

        for book_data in books_data:
            # Verificar si el libro ya existe por título y autor
            exists = db.query(Book).filter(
                Book.title == book_data["title"],
                Book.author == book_data["author"]
            ).first()
            if not exists:
                book = Book(**book_data)
                db.add(book)

        db.commit()
        print("✔ Datos iniciales insertados correctamente.")
    except IntegrityError as e:
        db.rollback()
        print("⚠ Error de integridad:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed()
