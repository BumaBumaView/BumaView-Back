import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///a.db"

Base = declarative_base()


class User(Base):
  __tablename__ = 'users'
  id = Column(String, primary_key=True)
  role = Column(String)
  password = Column(String)
  interviews = relationship("Interview", back_populates="user")


class Company(Base):
  __tablename__ = 'companies'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String, nullable=False)
  questions = relationship("Question", back_populates="company")


class Question(Base):
  __tablename__ = 'questions'
  question_id = Column(Integer, primary_key=True, autoincrement=True)
  questions = Column(String)
  parent = Column(Integer, ForeignKey('questions.question_id'))
  company_id = Column(Integer, ForeignKey('companies.id'))
  category = Column(String)
  question_at = Column(Integer)

  company = relationship("Company", back_populates="questions")
  parent_question = relationship("Question", remote_side=[question_id])


class Interview(Base):
  __tablename__ = 'interviews'
  id = Column(Integer, primary_key=True, autoincrement=True)
  eye_score = Column(Float)
  pose_score = Column(Float)
  answer_score = Column(Float)
  feedback = Column(String)
  interviewed_at = Column(Date, default=datetime.date.today)
  data = Column(String)
  student_id = Column(String, ForeignKey('users.id'))

  user = relationship("User", back_populates="interviews")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
  database = SessionLocal()
  try:
    yield database
  finally:
    database.close()


def create_tables():
  Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
  create_tables()
  print("Database tables created successfully.")
