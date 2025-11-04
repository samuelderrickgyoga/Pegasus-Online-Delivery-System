"""
Database Population Script for ODS (Online Delivery System)
Populates the database with sample data in the ratio 8:7:6:5:4:3:2:1
for Programs, Facilities, Equipment, Projects, Participants, Outcomes, Services, ProjectParticipants
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.program import Program
from app.models.facility import Facility
from app.models.equipment import Equipment
from app.models.project import Project
from app.models.participant import Participant
from app.models.outcome import Outcome
from app.models.service import Service
from app.models.project_participant import ProjectParticipant

def generate_date_range(start_days_ago=365, end_days_ago=0):
    """Generate a random date within the specified range"""
    start_date = datetime.now() - timedelta(days=start_days_ago)
    end_date = datetime.now() - timedelta(days=end_days_ago)
    time_between = end_date - start_date
    random_days = random.randrange(time_between.days)
    return start_date + timedelta(days=random_days)

def populate_programs(count=64):
    """Populate Programs - Ratio 8"""
    print(f"Creating {count} Programs...")
    
    program_templates = [
        {
            'name': 'Youth Skills Development',
            'description': 'Comprehensive skills training for youth aged 15-24',
            'national_alignment': 'National Youth Policy 2015',
            'focus_areas': 'Digital literacy, Leadership, Entrepreneurship',
            'phases': 'Phase 1: Orientation, Phase 2: Training, Phase 3: Internship'
        },
        {
            'name': 'Women Empowerment Initiative',
            'description': 'Economic empowerment program for rural women',
            'national_alignment': 'Gender Equality and Development Policy',
            'focus_areas': 'Financial literacy, Business management, Agriculture',
            'phases': 'Phase 1: Awareness, Phase 2: Training, Phase 3: Business startup'
        },
        {
            'name': 'Digital Transformation Program',
            'description': 'ICT capacity building for community members',
            'national_alignment': 'National ICT Policy',
            'focus_areas': 'Computer skills, Internet literacy, E-commerce',
            'phases': 'Phase 1: Basic training, Phase 2: Advanced skills, Phase 3: Certification'
        },
        {
            'name': 'Agricultural Modernization',
            'description': 'Modern farming techniques and technologies',
            'national_alignment': 'National Agriculture Policy',
            'focus_areas': 'Smart farming, Irrigation, Post-harvest handling',
            'phases': 'Phase 1: Training, Phase 2: Equipment distribution, Phase 3: Monitoring'
        },
        {
            'name': 'Community Health Program',
            'description': 'Healthcare access and health education',
            'national_alignment': 'National Health Policy',
            'focus_areas': 'Preventive care, Nutrition, Sanitation',
            'phases': 'Phase 1: Awareness, Phase 2: Training, Phase 3: Implementation'
        },
        {
            'name': 'Education Support Initiative',
            'description': 'Improving access to quality education',
            'national_alignment': 'Education Sector Strategic Plan',
            'focus_areas': 'Teacher training, Infrastructure, Learning materials',
            'phases': 'Phase 1: Assessment, Phase 2: Intervention, Phase 3: Evaluation'
        },
        {
            'name': 'Environmental Conservation',
            'description': 'Sustainable environment management practices',
            'national_alignment': 'National Environment Policy',
            'focus_areas': 'Tree planting, Waste management, Climate adaptation',
            'phases': 'Phase 1: Mobilization, Phase 2: Implementation, Phase 3: Monitoring'
        },
        {
            'name': 'Entrepreneurship Development',
            'description': 'Business startup support and mentorship',
            'national_alignment': 'National Entrepreneurship Policy',
            'focus_areas': 'Business planning, Access to finance, Market linkages',
            'phases': 'Phase 1: Training, Phase 2: Funding, Phase 3: Mentorship'
        }
    ]
    
    programs = []
    for i in range(count):
        template = program_templates[i % len(program_templates)]
        program = Program(
            name=f"{template['name']} {i+1}",
            description=f"{template['description']} (Cohort {i+1})",
            national_alignment=template['national_alignment'],
            focus_areas=template['focus_areas'],
            phases=template['phases']
        )
        programs.append(program)
        db.session.add(program)
    
    db.session.commit()
    print(f"✓ Created {count} Programs")
    return programs

def populate_facilities(count=56):
    """Populate Facilities - Ratio 7"""
    print(f"Creating {count} Facilities...")
    
    districts = ['Kampala', 'Wakiso', 'Mukono', 'Jinja', 'Mbarara', 'Gulu', 'Lira', 'Mbale']
    facility_types = ['Training Center', 'Workshop', 'Computer Lab', 'Conference Hall', 
                     'Resource Center', 'Community Hall', 'Innovation Hub']
    partners = ['USAID', 'World Bank', 'UNICEF', 'NGO Partnership', 'Government of Uganda', 'Private Sector']
    
    facilities = []
    for i in range(count):
        district = random.choice(districts)
        fac_type = random.choice(facility_types)
        capacity = random.randint(20, 200)
        
        facility = Facility(
            name=f"{district} {fac_type} {i+1}",
            location=f"{district} District, {random.choice(['Central', 'Northern', 'Eastern', 'Western'])} Region",
            description=f"Modern {fac_type.lower()} with capacity for {capacity} people",
            partner_org=random.choice(partners),
            facility_type=fac_type,
            capabilities=f"Projector, WiFi, {random.choice(['Air conditioning', 'Fans'])}, Furniture, {random.choice(['Kitchen', 'Cafeteria'])}"
        )
        facilities.append(facility)
        db.session.add(facility)
    
    db.session.commit()
    print(f"✓ Created {count} Facilities")
    return facilities

def populate_equipment(count=48):
    """Populate Equipment - Ratio 6"""
    print(f"Creating {count} Equipment...")
    
    equipment_types = [
        ('Laptop', 'Dell Latitude', 'Computing'),
        ('Projector', 'Epson EB-X41', 'Presentation'),
        ('Printer', 'HP LaserJet Pro', 'Office Equipment'),
        ('Tablet', 'Samsung Galaxy Tab', 'Computing'),
        ('Camera', 'Canon EOS', 'Photography'),
        ('Sewing Machine', 'Singer Industrial', 'Vocational Training'),
        ('Welding Machine', 'Miller Electric', 'Technical Training'),
        ('Carpentry Tools', 'Professional Set', 'Vocational Training'),
        ('Agricultural Equipment', 'Modern Farming Tools', 'Agriculture'),
        ('Medical Equipment', 'Healthcare Kit', 'Health Services')
    ]
    
    conditions = ['Excellent', 'Good', 'Fair', 'Need Repair']
    
    equipments = []
    
    # Get facilities for foreign key
    facilities = Facility.query.all()
    if not facilities:
        print("⚠ No facilities found. Creating equipment without facility assignment.")
        return equipments
    
    usage_domains = ['Electronics', 'Mechanical', 'IoT', 'Agriculture', 'Health', 'Education']
    support_phases = ['Training', 'Prototyping', 'Production', 'Maintenance', 'Research']
    
    for i in range(count):
        eq_type, model, category = random.choice(equipment_types)
        
        equipment = Equipment(
            facility_id=random.choice(facilities).id,
            name=f"{eq_type} {i+1}",
            capabilities=f"{model} with {random.choice(['basic', 'advanced', 'professional'])} features",
            description=f"{category} equipment for training and practical work",
            inventory_code=f"INV-{random.randint(10000, 99999)}-{i}",
            usage_domain=random.choice(usage_domains),
            support_phase=random.choice(support_phases)
        )
        equipments.append(equipment)
        db.session.add(equipment)
    
    db.session.commit()
    print(f"✓ Created {count} Equipment")
    return equipments

def populate_projects(count=40, programs=None, facilities=None):
    """Populate Projects - Ratio 5"""
    print(f"Creating {count} Projects...")
    
    natures = ['Training', 'Workshop', 'Mentorship', 'Research', 'Community Outreach']
    innovation_focuses = ['IoT Solutions', 'Mobile Apps', 'Green Energy', 'AgriTech', 'HealthTech', 'EdTech']
    prototype_stages = ['Concept', 'Design', 'Prototype', 'Testing', 'Production Ready']
    
    projects = []
    for i in range(count):
        program = random.choice(programs) if programs else None
        facility = random.choice(facilities) if facilities else None
        
        if not program or not facility:
            continue
        
        innovation = random.choice(innovation_focuses)
        
        project = Project(
            program_id=program.id,
            facility_id=facility.id,
            title=f"Project {i+1}: {random.choice(natures)} Initiative",
            nature=random.choice(natures),
            description=f"Comprehensive project focused on {innovation} and capacity building. Target beneficiaries: {random.randint(50, 500)} participants.",
            innovation_focus=innovation,
            prototype_stage=random.choice(prototype_stages),
            testing_requirements=f"Testing for {innovation} including performance, usability, and market validation",
            commercialization_plan=f"Phased rollout strategy with market research, pilot testing, and full-scale deployment"
        )
        projects.append(project)
        db.session.add(project)
    
    db.session.commit()
    print(f"✓ Created {len(projects)} Projects")
    return projects

def populate_participants(count=32):
    """Populate Participants - Ratio 4"""
    print(f"Creating {count} Participants...")
    
    first_names = ['John', 'Mary', 'David', 'Sarah', 'James', 'Grace', 'Peter', 'Agnes', 
                   'Michael', 'Ruth', 'Paul', 'Rebecca', 'Daniel', 'Esther', 'Joseph', 'Faith']
    last_names = ['Mugisha', 'Namukasa', 'Okello', 'Nakato', 'Kiiza', 'Atim', 'Wafula', 
                  'Aceng', 'Ssemakula', 'Nabirye', 'Tumwine', 'Apio', 'Byaruhanga', 'Aber']
    
    affiliations = ['CS', 'SE', 'IT', 'CE', 'EE', 'ME']
    specializations = ['Software Development', 'Hardware Engineering', 'Data Science', 'IoT', 'Embedded Systems']
    institutions = ['SCIT', 'CEDAT', 'CoCIS', 'Engineering', 'Sciences']
    
    participants = []
    for i in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        participant = Participant(
            full_name=f"{first_name} {last_name}",
            email=f"{first_name.lower()}.{last_name.lower()}{i}@students.mak.ac.ug",
            affiliation=random.choice(affiliations),
            specialization=random.choice(specializations),
            cross_skill_trained=random.choice([True, False]),
            institution=random.choice(institutions)
        )
        participants.append(participant)
        db.session.add(participant)
    
    db.session.commit()
    print(f"✓ Created {count} Participants")
    return participants

def populate_outcomes(count=24, projects=None):
    """Populate Outcomes - Ratio 3"""
    print(f"Creating {count} Outcomes...")
    
    outcome_types = ['CAD Design', 'PCB Layout', 'Prototype', 'Report', 'Software', 'Hardware']
    commercialization_statuses = ['Demoed', 'Launched', 'In Production', 'Market Ready', 'Under Development']
    certifications = ['UIRI Certified', 'ISO Compliant', 'Quality Tested', 'Industry Standard', 'Pending Certification']
    
    outcomes = []
    for i in range(count):
        project = random.choice(projects) if projects and len(projects) > 0 else None
        
        if not project:
            continue
        
        outcome_type = random.choice(outcome_types)
        
        outcome = Outcome(
            project_id=project.id,
            title=f"{outcome_type} Outcome for {project.title}",
            description=f"Comprehensive {outcome_type.lower()} deliverable achieving {random.randint(60, 98)}% of project objectives. Impact: {random.randint(50, 200)} beneficiaries.",
            artifact_link=f"https://artifacts.ods.mak.ac.ug/{outcome_type.lower()}/{i+1}",
            outcome_type=outcome_type,
            quality_certification=random.choice(certifications),
            commercialization_status=random.choice(commercialization_statuses)
        )
        outcomes.append(outcome)
        db.session.add(outcome)
    
    db.session.commit()
    print(f"✓ Created {len(outcomes)} Outcomes")
    return outcomes

def populate_services(count=16):
    """Populate Services - Ratio 2"""
    print(f"Creating {count} Services...")
    
    # Get facilities for foreign key
    facilities = Facility.query.all()
    if not facilities:
        print("⚠ No facilities found. Creating services without facility assignment.")
        return []
    
    service_templates = [
        ('Technical Training', 'Hands-on technical skills development', 'Training'),
        ('Business Mentorship', 'One-on-one business guidance and support', 'Mentorship'),
        ('Career Counseling', 'Professional career guidance and planning', 'Advisory'),
        ('Financial Advisory', 'Financial management and planning services', 'Advisory'),
        ('Legal Support', 'Legal advice and documentation assistance', 'Support'),
        ('Marketing Support', 'Product marketing and branding assistance', 'Support'),
        ('ICT Support', 'Technical support and digital services', 'Technical'),
        ('Agricultural Extension', 'Farming techniques and advisory services', 'Technical')
    ]
    
    skill_types = ['Software', 'Hardware', 'Business', 'Technical', 'Soft Skills', 'Research']
    
    services = []
    for i in range(count):
        template = service_templates[i % len(service_templates)]
        
        service = Service(
            facility_id=random.choice(facilities).id,
            name=f"{template[0]} {i+1}",
            description=template[1],
            category=template[2],
            skill_type=random.choice(skill_types)
        )
        services.append(service)
        db.session.add(service)
    
    db.session.commit()
    print(f"✓ Created {count} Services")
    return services

def populate_project_participants(count=8, projects=None, participants=None):
    """Populate Project Participants - Ratio 1"""
    print(f"Creating {count} Project-Participant relationships...")
    
    if not projects or not participants:
        print("⚠ Skipping Project Participants - missing projects or participants")
        return []
    
    roles_on_project = ['Student', 'Lecturer', 'Contributor', 'Intern', 'Researcher']
    skill_roles = ['Developer', 'Engineer', 'Designer', 'Business Lead', 'Project Manager', 'Analyst']
    
    project_participants = []
    used_combinations = set()
    
    attempts = 0
    max_attempts = count * 10
    
    while len(project_participants) < count and attempts < max_attempts:
        project = random.choice(projects)
        participant = random.choice(participants)
        combination = (project.id, participant.id)
        
        if combination not in used_combinations:
            pp = ProjectParticipant(
                project_id=project.id,
                participant_id=participant.id,
                role_on_project=random.choice(roles_on_project),
                skill_role=random.choice(skill_roles)
            )
            project_participants.append(pp)
            used_combinations.add(combination)
            db.session.add(pp)
        
        attempts += 1
    
    db.session.commit()
    print(f"✓ Created {len(project_participants)} Project-Participant relationships")
    return project_participants

def main():
    """Main function to populate the database"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("ODS DATABASE POPULATION SCRIPT")
        print("=" * 60)
        print(f"Ratio: 8:7:6:5:4:3:2:1")
        print(f"Base multiplier: 8")
        print(f"Total records: ~248 records")
        print("=" * 60)
        print()
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        response = input("Clear existing data? (yes/no): ")
        if response.lower() == 'yes':
            print("\nClearing existing data...")
            ProjectParticipant.query.delete()
            Outcome.query.delete()
            Service.query.delete()
            Project.query.delete()
            Participant.query.delete()
            Equipment.query.delete()
            Facility.query.delete()
            Program.query.delete()
            db.session.commit()
            print("✓ Database cleared")
        
        print("\nPopulating database with sample data...")
        print()
        
        # Populate in order (respecting foreign key constraints)
        programs = populate_programs(64)  # 8 * 8
        facilities = populate_facilities(56)  # 7 * 8
        equipment = populate_equipment(48)  # 6 * 8
        projects = populate_projects(40, programs, facilities)  # 5 * 8
        participants = populate_participants(32)  # 4 * 8
        outcomes = populate_outcomes(24, projects)  # 3 * 8
        services = populate_services(16)  # 2 * 8
        project_participants = populate_project_participants(8, projects, participants)  # 1 * 8
        
        print()
        print("=" * 60)
        print("DATABASE POPULATION COMPLETE!")
        print("=" * 60)
        print(f"Programs: {len(programs)}")
        print(f"Facilities: {len(facilities)}")
        print(f"Equipment: {len(equipment)}")
        print(f"Projects: {len(projects)}")
        print(f"Participants: {len(participants)}")
        print(f"Outcomes: {len(outcomes)}")
        print(f"Services: {len(services)}")
        print(f"Project-Participants: {len(project_participants)}")
        print(f"TOTAL RECORDS: {len(programs) + len(facilities) + len(equipment) + len(projects) + len(participants) + len(outcomes) + len(services) + len(project_participants)}")
        print("=" * 60)

if __name__ == '__main__':
    main()
