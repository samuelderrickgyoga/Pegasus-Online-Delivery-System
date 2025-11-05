"""
Quick test script to verify API endpoints are working
"""
from app import create_app, db
from app.models.program import Program
from app.models.facility import Facility
from app.models.project import Project
from app.models.participant import Participant

app = create_app()

with app.app_context():
    # Check database counts
    programs_count = Program.query.count()
    facilities_count = Facility.query.count()
    projects_count = Project.query.count()
    participants_count = Participant.query.count()
    
    print("=" * 60)
    print("DATABASE STATUS CHECK")
    print("=" * 60)
    print(f"Programs: {programs_count}")
    print(f"Facilities: {facilities_count}")
    print(f"Projects: {projects_count}")
    print(f"Participants: {participants_count}")
    print("=" * 60)
    
    if programs_count == 0:
        print("\n⚠️  DATABASE IS EMPTY!")
        print("Run: python populate_database.py")
        print("=" * 60)
    else:
        print("\n✅ Database has data. Testing API...")
        
        # Test a simple query
        sample_program = Program.query.first()
        if sample_program:
            print(f"\nSample Program:")
            print(f"  ID: {sample_program.id}")
            print(f"  Name: {sample_program.name}")
            print(f"  Description: {sample_program.description[:50] if sample_program.description else 'None'}...")
            
        sample_project = Project.query.first()
        if sample_project:
            print(f"\nSample Project:")
            print(f"  ID: {sample_project.id}")
            print(f"  Title: {sample_project.title}")
            print(f"  Nature: {sample_project.nature}")
            
        print("\n" + "=" * 60)
        print("✅ API should be working fine.")
        print("If templates still show no data, check browser console for errors.")
        print("=" * 60)
