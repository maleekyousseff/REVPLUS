from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError



# Créer un moteur de base de données SQLite
engine = create_engine('sqlite:///revplus.db', echo=True)
Base = declarative_base()

# Créer une session de base de données
Session = sessionmaker(bind=engine)
session = Session()

# Définir le modèle de la base de données
class PDFDocument(Base):
    __tablename__ = 'pdf_documents'

    id = Column(Integer, primary_key=True)
    file_name = Column(String, unique=True)
    text = Column(Text)

# Définir le modèle de la base de données pour les utilisateurs
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)  # Note: Utilisez un hachage de mot de passe sécurisé dans une vraie application

# Créer les tables
Base.metadata.create_all(engine)

# Fonction pour ajouter un document PDF
def add_pdf_document(file_name, text):
    try:
         pdf_document = PDFDocument(file_name=file_name, text=text)
         session.add(pdf_document)
         session.commit()
    except IntegrityError:
        session.rollback()
        print(f"Le document avec le nom de fichier '{file_name}' existe déjà.")


# Fonction pour récupérer un document PDF par nom de fichier
def get_pdf_document(file_name):
    return session.query(PDFDocument).filter_by(file_name=file_name).first()
# Fonction pour récupérer tous les documents PDF

def get_all_pdf_documents():
    return session.query(PDFDocument).all()

# Fonction pour ajouter un utilisateur
def add_user(username, password):
    try:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
    except IntegrityError:
        session.rollback()
        print(f"L'utilisateur avec le nom '{username}' existe déjà.")
        
# Fonction pour vérifier les informations de connexion de l'utilisateur
def authenticate_user(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    return user is not None        