from fastapi.testclient import TestClient
from main import app
from sqlalchemy import StaticPool
from core.database import Base, create_engine, sessionmaker, get_db
import pytest
from faker import Faker
from expenses.models import ExpenseModel
from users.models import UserModel
from people.models import PersonModel
from auth.jwt_auth import generate_access_token
from core.i18n import load_translations

fake = Faker()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="package", autouse=True)
def load_langs():
    load_translations()


@pytest.fixture(scope="module", autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session  # type: ignore
    yield
    app.dependency_overrides.pop(get_db, None)  # type: ignore


@pytest.fixture(scope="session", autouse=True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)  # creates all the models in the memory
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="package")
def anonymous_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="package", autouse=True)
def generate_mock_data(db_session):
    person = PersonModel(first_name=fake.first_name(), last_name=fake.last_name())
    db_session.add(person)
    db_session.commit()
    db_session.refresh(person)
    user = UserModel(username="testuser", person_id=person.id)
    user.set_password("12345678")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"User created with username: {user.username} and ID: {user.id}")
    expenses_list = []
    for _ in range(10):
        expenses_list.append(
            ExpenseModel(
                person_id=person.id,
                description=fake.text(40),
                amount=fake.random_number(),
            )
        )
    db_session.add_all(expenses_list)
    db_session.commit()
    print(f"added 10 expenses for user id {user.id}")


@pytest.fixture(scope="module")
def auth_client(db_session):
    client = TestClient(app)
    user = db_session.query(UserModel).filter_by(username="testuser").one_or_none()
    access_token = generate_access_token(user.id)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client


@pytest.fixture(scope="function")
def random_expense(db_session):
    user = db_session.query(UserModel).filter_by(username="testuser").one_or_none()
    person = db_session.query(PersonModel).filter_by(id=user.person_id).one_or_none()
    expense = db_session.query(ExpenseModel).filter_by(person_id=person.id).first()
    return expense
