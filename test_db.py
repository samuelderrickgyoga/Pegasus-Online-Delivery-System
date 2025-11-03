from app import create_app, db
from app.models.program import Program

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created")

    # Add a test record
    program = Program(name="Test Program", description="A test program")
    db.session.add(program)
    db.session.commit()
    print("Test program added")

    # Query it
    programs = Program.query.all()
    print(f"Programs in DB: {len(programs)}")
    for p in programs:
        print(f"ID: {p.id}, Name: {p.name}")
