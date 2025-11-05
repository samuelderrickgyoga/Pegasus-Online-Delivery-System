"""
Diagnostic script to identify and fix template data loading issues
"""
import sys
from app import create_app, db
from app.models.program import Program
from app.models.facility import Facility
from app.models.project import Project
from app.models.participant import Participant
from app.models.equipment import Equipment
from app.models.outcome import Outcome
from app.models.service import Service

def check_database():
    """Check if database exists and has data"""
    app = create_app()
    
    with app.app_context():
        try:
            counts = {
                'Programs': Program.query.count(),
                'Facilities': Facility.query.count(),
                'Equipment': Equipment.query.count(),
                'Projects': Project.query.count(),
                'Participants': Participant.query.count(),
                'Outcomes': Outcome.query.count(),
                'Services': Service.query.count()
            }
            
            print("\n" + "="*70)
            print(" DATABASE STATUS CHECK ".center(70, "="))
            print("="*70)
            
            total = sum(counts.values())
            
            for entity, count in counts.items():
                status = "✅" if count > 0 else "❌"
                print(f"{status} {entity:15} : {count:5} records")
            
            print("="*70)
            print(f"TOTAL RECORDS: {total}")
            print("="*70)
            
            if total == 0:
                print("\n🚨 DATABASE IS EMPTY!")
                print("\nTO FIX:")
                print("  1. Run: python populate_database.py")
                print("  2. Wait for it to complete")
                print("  3. Run: python run.py")
                print("  4. Open browser to http://127.0.0.1:5000")
                return False
            else:
                print("\n✅ DATABASE HAS DATA")
                
                # Show sample data
                print("\n" + "="*70)
                print(" SAMPLE DATA ".center(70, "="))
                print("="*70)
                
                program = Program.query.first()
                if program:
                    print(f"\n📋 Sample Program:")
                    print(f"   ID: {program.id}")
                    print(f"   Name: {program.name}")
                
                project = Project.query.first()
                if project:
                    print(f"\n🔬 Sample Project:")
                    print(f"   ID: {project.id}")
                    print(f"   Title: {project.title}")
                    print(f"   Nature: {project.nature}")
                
                participant = Participant.query.first()
                if participant:
                    print(f"\n👤 Sample Participant:")
                    print(f"   ID: {participant.id}")
                    print(f"   Name: {participant.full_name}")
                    print(f"   Email: {participant.email}")
                
                print("\n" + "="*70)
                print("\n✅ DATA IS AVAILABLE")
                print("\nNEXT STEPS:")
                print("  1. Run: python run.py")
                print("  2. Open browser to http://127.0.0.1:5000")
                print("  3. Navigate to Projects, Programs, etc.")
                print("  4. Check browser console (F12) for any JavaScript errors")
                print("\n" + "="*70)
                return True
                
        except Exception as e:
            print(f"\n❌ ERROR checking database: {str(e)}")
            print("\nThe database might not be initialized.")
            print("Try running: python populate_database.py")
            return False

if __name__ == "__main__":
    check_database()
