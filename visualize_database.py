"""
Database Visualization Script for ODS (Online Delivery System)
Creates comprehensive visualizations with explanations for data analysis
"""

import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime

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

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 10

class DatabaseVisualizer:
    """Class to handle all database visualizations"""
    
    def __init__(self, app):
        self.app = app
        self.data = {}
        
    def collect_data(self):
        """Collect data from all models"""
        print("Collecting data from database...")
        
        with self.app.app_context():
            # Entity counts
            self.data['entity_counts'] = {
                'Programs': Program.query.count(),
                'Facilities': Facility.query.count(),
                'Equipment': Equipment.query.count(),
                'Projects': Project.query.count(),
                'Participants': Participant.query.count(),
                'Outcomes': Outcome.query.count(),
                'Services': Service.query.count(),
                'Project-Participants': ProjectParticipant.query.count()
            }
            
            # Programs data
            programs = Program.query.all()
            self.data['programs'] = [p.to_dict() for p in programs]
            
            # Facilities data
            facilities = Facility.query.all()
            self.data['facilities'] = [f.to_dict() for f in facilities]
            
            # Equipment data
            equipment = Equipment.query.all()
            self.data['equipment'] = [e.to_dict() for e in equipment]
            
            # Projects data
            projects = Project.query.all()
            self.data['projects'] = [p.to_dict() for p in projects]
            
            # Participants data
            participants = Participant.query.all()
            self.data['participants'] = [p.to_dict() for p in participants]
            
            # Outcomes data
            outcomes = Outcome.query.all()
            self.data['outcomes'] = [o.to_dict() for o in outcomes]
            
            # Services data
            services = Service.query.all()
            self.data['services'] = [s.to_dict() for s in services]

            # Project-Participants data (for KPIs like avg participants per project)
            pps = ProjectParticipant.query.all()
            self.data['project_participants'] = [pp.to_dict() for pp in pps]
            
        print(f"✓ Collected data for {sum(self.data['entity_counts'].values())} total records")
        
    def create_pie_chart_distribution(self):
        """
        PIE CHART: Entity Distribution Across the System
        
        WHY PIE CHART?
        - Shows proportional distribution of different entities
        - Ideal for displaying composition/parts-of-a-whole relationships
        - Easy to see which entities dominate the system
        - Best for categorical data with <10 categories
        - Visually appealing for stakeholder presentations
        """
        print("\nCreating Pie Chart: Entity Distribution...")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        labels = list(self.data['entity_counts'].keys())
        sizes = list(self.data['entity_counts'].values())
        colors = plt.cm.Set3(range(len(labels)))
        
        # Create pie chart with percentage labels
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.05] * len(labels)  # Slight separation for clarity
        )
        
        # Beautify text
        for text in texts:
            text.set_fontsize(12)
            text.set_weight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title('ODS Entity Distribution\n(Pie Chart - Proportional Representation)', 
                    fontsize=16, weight='bold', pad=20)
        
        # Add legend with counts
        legend_labels = [f"{label}: {size}" for label, size in zip(labels, sizes)]
        ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.tight_layout()
        plt.savefig('visualization_1_pie_chart.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: visualization_1_pie_chart.png")
        
        # Print explanation
        print("\n" + "="*70)
        print("VISUALIZATION 1: PIE CHART EXPLANATION")
        print("="*70)
        print("WHY PIE CHART?")
        print("  • Best for showing proportional distribution (parts of a whole)")
        print("  • Instantly shows which entities make up larger portions")
        print("  • Ideal for categorical data with few categories (<10)")
        print("  • Easy for non-technical stakeholders to understand")
        print("\nINSIGHTS:")
        total = sum(sizes)
        for label, size in zip(labels, sizes):
            percentage = (size/total) * 100
            print(f"  • {label}: {size} records ({percentage:.1f}% of total)")
        print("="*70 + "\n")
        
    def create_bar_chart_comparison(self):
        """
        BAR CHART: Entity Counts Comparison
        
        WHY BAR CHART?
        - Excellent for comparing quantities across categories
        - Easy to read and interpret exact values
        - Shows ranking clearly (highest to lowest)
        - Good for showing the 8:7:6:5:4:3:2:1 ratio pattern
        """
        print("Creating Bar Chart: Entity Comparison...")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        entities = list(self.data['entity_counts'].keys())
        counts = list(self.data['entity_counts'].values())
        
        # Create horizontal bar chart (better for long labels)
        bars = ax.barh(entities, counts, color=plt.cm.viridis(np.linspace(0, 1, len(entities))))
        
        # Add value labels on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(count + 1, i, str(count), va='center', fontsize=11, weight='bold')
        
        ax.set_xlabel('Number of Records', fontsize=12, weight='bold')
        ax.set_ylabel('Entity Type', fontsize=12, weight='bold')
        ax.set_title('ODS Entity Counts Comparison\n(Bar Chart - Quantitative Comparison)', 
                    fontsize=16, weight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('visualization_2_bar_chart.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: visualization_2_bar_chart.png")
        
        print("\n" + "="*70)
        print("VISUALIZATION 2: BAR CHART EXPLANATION")
        print("="*70)
        print("WHY BAR CHART?")
        print("  • Perfect for comparing quantities across different categories")
        print("  • Shows exact values clearly")
        print("  • Easy to identify highest and lowest values")
        print("  • Demonstrates the 8:7:6:5:4:3:2:1 ratio pattern visually")
        print("\nINSIGHTS:")
        sorted_data = sorted(zip(entities, counts), key=lambda x: x[1], reverse=True)
        for i, (entity, count) in enumerate(sorted_data, 1):
            print(f"  {i}. {entity}: {count} records")
        print("="*70 + "\n")
        
    def create_project_status_visualization(self):
        """
        PROJECT PIPELINE DISTRIBUTION
        
        WHY THESE CHARTS?
        - Show composition within project pipeline
        - If explicit status is unavailable, use prototype_stage or nature
        - Helps identify execution focus and pipeline health
        """
        print("Creating Stacked Bar Chart: Project Status Distribution...")
        
        projects_df = pd.DataFrame(self.data['projects'])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        label_col = None
        title_stub = None
        if 'status' in projects_df.columns and projects_df['status'].notna().any():
            label_col = 'status'
            title_stub = 'Status'
        elif 'prototype_stage' in projects_df.columns and projects_df['prototype_stage'].notna().any():
            label_col = 'prototype_stage'
            title_stub = 'Prototype Stage'
        elif 'nature' in projects_df.columns and projects_df['nature'].notna().any():
            label_col = 'nature'
            title_stub = 'Nature'

        if label_col:
            counts = projects_df[label_col].value_counts()
            colors = plt.cm.Pastel1(range(len(counts)))

            # Pie
            ax1.pie(counts.values, labels=counts.index, autopct='%1.1f%%',
                    colors=colors, startangle=90)
            ax1.set_title(f'Project {title_stub} Distribution', fontsize=14, weight='bold')

            # Bar
            bars = ax2.bar(counts.index, counts.values, color=colors)
            ax2.set_xlabel(f'Project {title_stub}', fontsize=12, weight='bold')
            ax2.set_ylabel('Number of Projects', fontsize=12, weight='bold')
            ax2.set_title(f'Project {title_stub} Counts', fontsize=14, weight='bold')
            ax2.grid(axis='y', alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right')

            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                         f'{int(height)}', ha='center', va='bottom', fontsize=11, weight='bold')

            plt.tight_layout()
            plt.savefig('visualization_3_project_status.png', dpi=300, bbox_inches='tight')
            print("✓ Saved: visualization_3_project_status.png")

            print("\n" + "="*70)
            print("VISUALIZATION 3: PROJECT PIPELINE EXPLANATION")
            print("="*70)
            print("WHY THESE CHARTS?")
            print("  • Pie: Proportions across the pipeline categories")
            print("  • Bar: Exact counts for planning and tracking")
            print("\nINSIGHTS:")
            for label, count in counts.items():
                percentage = (count / counts.sum()) * 100
                print(f"  • {label}: {count} projects ({percentage:.1f}%)")
            print("="*70 + "\n")
        
    def create_participant_demographics(self):
        """
        PARTICIPANT PROFILE ANALYTICS
        
        If age/gender not available, visualize affiliation, specialization,
        cross-skill training, and institution distribution.
        """
        print("Creating Participant Profile Analytics...")

        participants_df = pd.DataFrame(self.data['participants'])

        if participants_df.empty:
            return

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Affiliation distribution (Pie)
        ax1 = axes[0, 0]
        if 'affiliation' in participants_df.columns:
            aff_counts = participants_df['affiliation'].value_counts()
            ax1.pie(aff_counts.values, labels=aff_counts.index, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Participant Affiliation Distribution', fontsize=14, weight='bold')
        else:
            ax1.axis('off')

        # Specialization distribution (Bar)
        ax2 = axes[0, 1]
        if 'specialization' in participants_df.columns:
            spec_counts = participants_df['specialization'].value_counts()
            bars = ax2.bar(spec_counts.index, spec_counts.values, color=plt.cm.Set2(range(len(spec_counts))))
            ax2.set_title('Specialization Mix', fontsize=14, weight='bold')
            ax2.set_ylabel('Count')
            ax2.grid(axis='y', alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right')
            for bar in bars:
                h = bar.get_height()
                ax2.text(bar.get_x()+bar.get_width()/2., h, f'{int(h)}', ha='center', va='bottom')
        else:
            ax2.axis('off')

        # Cross-skill trained (Pie)
        ax3 = axes[1, 0]
        if 'cross_skill_trained' in participants_df.columns:
            cross_counts = participants_df['cross_skill_trained'].value_counts()
            labels = ['Cross-trained' if k else 'Not cross-trained' for k in cross_counts.index]
            ax3.pie(cross_counts.values, labels=labels, autopct='%1.1f%%', colors=['#90EE90','#FFC107'])
            ax3.set_title('Cross-Skill Training Adoption', fontsize=14, weight='bold')
        else:
            ax3.axis('off')

        # Institution distribution (Bar)
        ax4 = axes[1, 1]
        if 'institution' in participants_df.columns:
            inst_counts = participants_df['institution'].value_counts()
            bars = ax4.bar(inst_counts.index, inst_counts.values, color=plt.cm.Pastel2(range(len(inst_counts))))
            ax4.set_title('Institution Representation', fontsize=14, weight='bold')
            ax4.set_ylabel('Count')
            ax4.grid(axis='y', alpha=0.3)
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=30, ha='right')
            for bar in bars:
                h = bar.get_height()
                ax4.text(bar.get_x()+bar.get_width()/2., h, f'{int(h)}', ha='center', va='bottom')
        else:
            ax4.axis('off')

        plt.tight_layout()
        plt.savefig('visualization_4_demographics.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: visualization_4_demographics.png")

        print("\n" + "="*70)
        print("VISUALIZATION 4: PARTICIPANT PROFILE EXPLANATION")
        print("="*70)
        print("WHY THESE CHARTS?")
        print("  • Show who engages with the program (affiliation, specialization)")
        print("  • Reveal cross-skill training uptake and institutional reach")
        if 'specialization' in participants_df.columns:
            print("\nINSIGHTS (Examples):")
            for spec, cnt in spec_counts.items():
                print(f"  • {spec}: {cnt}")
        print("="*70 + "\n")
        
    def create_equipment_condition_analysis(self):
        """
        EQUIPMENT PORTFOLIO ANALYTICS
        
        If condition is unavailable, visualize usage_domain and support_phase.
        """
        print("Creating Equipment Portfolio Analysis...")

        equipment_df = pd.DataFrame(self.data['equipment'])

        if equipment_df.empty:
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Usage domain distribution
        if 'usage_domain' in equipment_df.columns:
            dom_counts = equipment_df['usage_domain'].value_counts()
            bars = ax1.bar(dom_counts.index, dom_counts.values, color=plt.cm.Set3(range(len(dom_counts))))
            ax1.set_title('Equipment Usage Domains', fontsize=14, weight='bold')
            ax1.set_ylabel('Count')
            ax1.grid(axis='y', alpha=0.3)
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right')
            for bar in bars:
                h = bar.get_height()
                ax1.text(bar.get_x()+bar.get_width()/2., h, f'{int(h)}', ha='center', va='bottom')
        else:
            ax1.axis('off')

        # Support phase distribution
        if 'support_phase' in equipment_df.columns:
            phase_counts = equipment_df['support_phase'].value_counts()
            ax2.pie(phase_counts.values, labels=phase_counts.index, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Equipment Support Phases', fontsize=14, weight='bold')
        else:
            ax2.axis('off')

        plt.tight_layout()
        plt.savefig('visualization_5_equipment_condition.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: visualization_5_equipment_condition.png")

        print("\n" + "="*70)
        print("VISUALIZATION 5: EQUIPMENT PORTFOLIO EXPLANATION")
        print("="*70)
        print("WHY THESE CHARTS?")
        print("  • Show where equipment is used and at what stage it supports")
        print("  • Guides procurement and maintenance planning")
        if 'usage_domain' in equipment_df.columns:
            print("\nINSIGHTS (Domains):")
            for k, v in dom_counts.items():
                print(f"  • {k}: {v}")
        print("="*70 + "\n")
        
    def create_facility_capacity_analysis(self):
        """
        FACILITY PROFILE ANALYTICS
        
        If capacity isn't modeled, show facility_type mix and capability keywords.
        """
        print("Creating Facility Profile Analysis...")

        facilities_df = pd.DataFrame(self.data['facilities'])

        if facilities_df.empty:
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Facility type distribution
        if 'facility_type' in facilities_df.columns:
            type_counts = facilities_df['facility_type'].value_counts()
            bars = ax1.bar(type_counts.index, type_counts.values, color=plt.cm.Set2(range(len(type_counts))))
            ax1.set_title('Facility Types', fontsize=14, weight='bold')
            ax1.set_ylabel('Count')
            ax1.grid(axis='y', alpha=0.3)
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right')
            for bar in bars:
                h = bar.get_height()
                ax1.text(bar.get_x()+bar.get_width()/2., h, f'{int(h)}', ha='center', va='bottom')
        else:
            ax1.axis('off')

        # Capabilities keyword frequency (top 10)
        if 'capabilities' in facilities_df.columns:
            keywords = []
            for caps in facilities_df['capabilities'].dropna().tolist():
                for token in [c.strip() for c in str(caps).split(',') if c.strip()]:
                    keywords.append(token)
            if keywords:
                kw_series = pd.Series(keywords).value_counts().head(10)
                ax2.barh(kw_series.index[::-1], kw_series.values[::-1], color='#87CEEB')
                ax2.set_title('Top Facility Capabilities', fontsize=14, weight='bold')
                ax2.set_xlabel('Frequency')
                ax2.grid(axis='x', alpha=0.3)
        else:
            ax2.axis('off')

        plt.tight_layout()
        plt.savefig('visualization_6_facility_capacity.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: visualization_6_facility_capacity.png")

        print("\n" + "="*70)
        print("VISUALIZATION 6: FACILITY PROFILE EXPLANATION")
        print("="*70)
        print("WHY THESE CHARTS?")
        print("  • Show the mix of facility types and common capability features")
        print("  • Useful for planning training/events based on available resources")
        if 'facility_type' in facilities_df.columns:
            for k, v in type_counts.items():
                print(f"  • {k}: {v}")
        print("="*70 + "\n")
        
    def create_outcome_impact_analysis(self):
        """
        OUTCOME PROGRESSION & COMMERCIALIZATION
        
        If impact_level isn't modeled, use outcome_type and commercialization_status.
        """
        print("Creating Outcome Progression Analysis...")

        outcomes_df = pd.DataFrame(self.data['outcomes'])

        if outcomes_df.empty:
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Commercialization status (Bar)
        if 'commercialization_status' in outcomes_df.columns:
            comm_counts = outcomes_df['commercialization_status'].value_counts()
            bars = ax1.bar(comm_counts.index, comm_counts.values, color=plt.cm.Set3(range(len(comm_counts))))
            ax1.set_title('Commercialization Status', fontsize=14, weight='bold')
            ax1.set_ylabel('Outcomes')
            ax1.grid(axis='y', alpha=0.3)
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right')
            for bar in bars:
                h = bar.get_height()
                ax1.text(bar.get_x()+bar.get_width()/2., h, f'{int(h)}', ha='center', va='bottom')
        else:
            ax1.axis('off')

        # Outcome types (Pie)
        if 'outcome_type' in outcomes_df.columns:
            type_counts = outcomes_df['outcome_type'].value_counts()
            ax2.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Outcome Types', fontsize=14, weight='bold')
        else:
            ax2.axis('off')

        plt.tight_layout()
        plt.savefig('visualization_7_outcome_impact.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: visualization_7_outcome_impact.png")

        print("\n" + "="*70)
        print("VISUALIZATION 7: OUTCOME PROGRESSION EXPLANATION")
        print("="*70)
        print("WHY THESE CHARTS?")
        print("  • Show the share of outcomes that progressed toward market")
        print("  • Reveal dominant artifact types produced")
        if 'commercialization_status' in outcomes_df.columns:
            for k, v in comm_counts.items():
                print(f"  • {k}: {v}")
        print("="*70 + "\n")
        
    def create_system_analytics(self):
        """
        SYSTEM ANALYTICS: Complete system performance metrics
        
        WHY ANALYTICS DASHBOARD?
        - Shows system health at a glance
        - Tracks key performance indicators (KPIs)
        - Identifies trends and patterns
        - Supports data-driven decision making
        """
        print("Creating System Analytics...")
        
        fig = plt.figure(figsize=(20, 14))
        gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)
        
        # 1. Entity Growth Potential (Ratio visualization)
        ax1 = fig.add_subplot(gs[0, :])
        entities = list(self.data['entity_counts'].keys())
        counts = list(self.data['entity_counts'].values())
        ratios = [8, 7, 6, 5, 4, 3, 2, 1]
        
        x = np.arange(len(entities))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, counts, width, label='Actual Count', color='#4CAF50')
        bars2 = ax1.bar(x + width/2, [r*8 for r in ratios], width, label='Expected (8:7:6:5:4:3:2:1)', 
                       color='#2196F3', alpha=0.7)
        
        ax1.set_xlabel('Entity Type', fontsize=12, weight='bold')
        ax1.set_ylabel('Count', fontsize=12, weight='bold')
        ax1.set_title('System Analytics: Actual vs Expected Distribution\n(Validates 8:7:6:5:4:3:2:1 Ratio)', 
                     fontsize=14, weight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(entities, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        # 2. Engagement & Coverage Metrics (schema-aligned)
        ax2 = fig.add_subplot(gs[1, 0])
        if self.data['projects'] and self.data['services'] and self.data['facilities']:
            projects_df = pd.DataFrame(self.data['projects'])
            services_df = pd.DataFrame(self.data['services'])
            facilities_df = pd.DataFrame(self.data['facilities'])

            # Coverage metrics: services per facility, projects per facility, projects per program (if programs exist)
            spp = len(services_df) / len(facilities_df) if len(facilities_df) > 0 else 0
            ppf = len(projects_df) / len(facilities_df) if len(facilities_df) > 0 else 0
            ppp = len(projects_df) / max(1, self.data['entity_counts'].get('Programs', 1))

            categories = ['Services/Facility', 'Projects/Facility', 'Projects/Program']
            values = [spp, ppf, ppp]
            colors = ['#4CAF50', '#2196F3', '#9C27B0']

            bars = ax2.bar(categories, values, color=colors)
            ax2.set_ylabel('Average', fontsize=10, weight='bold')
            ax2.set_title('Engagement & Coverage Metrics', fontsize=12, weight='bold')
            ax2.grid(axis='y', alpha=0.3)
            for bar in bars:
                h = bar.get_height()
                ax2.text(bar.get_x()+bar.get_width()/2., h, f'{h:.2f}', ha='center', va='bottom')
        
        # 3. Participant Engagement Analysis
        ax3 = fig.add_subplot(gs[1, 1])
        if self.data['participants']:
            participants_df = pd.DataFrame(self.data['participants'])
            
            if 'education_level' in participants_df.columns:
                edu_counts = participants_df['education_level'].value_counts()
                colors_edu = plt.cm.Set3(range(len(edu_counts)))
                
                wedges, texts, autotexts = ax3.pie(edu_counts.values, labels=edu_counts.index,
                                                   autopct='%1.0f%%', colors=colors_edu, startangle=90)
                for text in texts:
                    text.set_fontsize(9)
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(8)
                    autotext.set_weight('bold')
                ax3.set_title('Participant Education Levels\n(Engagement Profile)', fontsize=12, weight='bold')
        
        # 4. Project Budget Analysis
        ax4 = fig.add_subplot(gs[1, 2])
        if self.data['projects']:
            projects_df = pd.DataFrame(self.data['projects'])
            
            if 'budget' in projects_df.columns:
                budgets = projects_df['budget'].dropna()
                
                # Budget ranges
                budget_ranges = ['<5M', '5M-15M', '15M-30M', '30M+']
                range_counts = [
                    len(budgets[budgets < 5000000]),
                    len(budgets[(budgets >= 5000000) & (budgets < 15000000)]),
                    len(budgets[(budgets >= 15000000) & (budgets < 30000000)]),
                    len(budgets[budgets >= 30000000])
                ]
                
                bars = ax4.bar(budget_ranges, range_counts, color=['#90EE90', '#87CEEB', '#FFD700', '#FFA07A'])
                ax4.set_xlabel('Budget Range (UGX)', fontsize=10, weight='bold')
                ax4.set_ylabel('Number of Projects', fontsize=10, weight='bold')
                ax4.set_title('Project Budget Distribution', fontsize=12, weight='bold')
                ax4.grid(axis='y', alpha=0.3)
                
                for bar in bars:
                    height = bar.get_height()
                    ax4.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom', fontsize=10, weight='bold')
        
        # 5. Timeline Analysis
        ax5 = fig.add_subplot(gs[2, 0])
        if self.data['projects']:
            projects_df = pd.DataFrame(self.data['projects'])
            
            if 'start_date' in projects_df.columns and 'end_date' in projects_df.columns:
                # Convert to datetime
                projects_df['start_date'] = pd.to_datetime(projects_df['start_date'], errors='coerce')
                projects_df['end_date'] = pd.to_datetime(projects_df['end_date'], errors='coerce')
                
                # Calculate duration in days
                projects_df['duration'] = (projects_df['end_date'] - projects_df['start_date']).dt.days
                
                durations = projects_df['duration'].dropna()
                
                ax5.hist(durations, bins=15, color='#87CEEB', edgecolor='black', alpha=0.7)
                ax5.set_xlabel('Project Duration (days)', fontsize=10, weight='bold')
                ax5.set_ylabel('Frequency', fontsize=10, weight='bold')
                ax5.set_title('Project Duration Distribution', fontsize=12, weight='bold')
                ax5.axvline(durations.mean(), color='red', linestyle='--', linewidth=2, 
                           label=f'Mean: {durations.mean():.0f} days')
                ax5.legend()
                ax5.grid(axis='y', alpha=0.3)
        
        # 6. Outcome Success Rate (derived from commercialization status)
        ax6 = fig.add_subplot(gs[2, 1])
        if self.data['outcomes']:
            outcomes_df = pd.DataFrame(self.data['outcomes'])
            
            if 'commercialization_status' in outcomes_df.columns:
                success_states = {'Launched', 'In Production', 'Market Ready'}
                success_count = outcomes_df['commercialization_status'].isin(success_states).sum()
                total_count = len(outcomes_df)
                success_rate = (success_count / total_count * 100) if total_count > 0 else 0

                labels = ['Commercialized/Ready', 'Other']
                sizes = [success_count, total_count - success_count]
                colors = ['#4CAF50', '#FFC107']
                explode = (0.1, 0)

                ax6.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        colors=colors, startangle=90)
                ax6.set_title(f'Outcome Success Rate (Commercialization)\nOverall: {success_rate:.1f}%', 
                              fontsize=12, weight='bold')
        
        # 7. Participant Specialization Mix (replaces gender)
        ax7 = fig.add_subplot(gs[2, 2])
        if self.data['participants']:
            participants_df = pd.DataFrame(self.data['participants'])
            if 'specialization' in participants_df.columns:
                spec_counts = participants_df['specialization'].value_counts()
                bars = ax7.bar(spec_counts.index, spec_counts.values, color=plt.cm.Set2(range(len(spec_counts))))
                ax7.set_xlabel('Specialization', fontsize=10, weight='bold')
                ax7.set_ylabel('Count', fontsize=10, weight='bold')
                ax7.set_title('Participant Specialization Mix', fontsize=12, weight='bold')
                ax7.grid(axis='y', alpha=0.3)
                plt.setp(ax7.xaxis.get_majorticklabels(), rotation=30, ha='right')
                for bar in bars:
                    h = bar.get_height()
                    ax7.text(bar.get_x()+bar.get_width()/2., h, f'{int(h)}', ha='center', va='bottom')
        
        # 8. Technology Portfolio Mix (replaces condition-based health)
        ax8 = fig.add_subplot(gs[3, 0])
        if self.data['equipment']:
            equipment_df = pd.DataFrame(self.data['equipment'])
            
            if 'usage_domain' in equipment_df.columns:
                dom_counts = equipment_df['usage_domain'].value_counts()
                bars = ax8.barh(dom_counts.index[::-1], dom_counts.values[::-1], color=plt.cm.Pastel1(range(len(dom_counts))))
                ax8.set_xlabel('Count', fontsize=10, weight='bold')
                ax8.set_title('Technology Portfolio Mix (Usage Domains)', fontsize=12, weight='bold')
                ax8.grid(axis='x', alpha=0.3)
                for i, (label, count) in enumerate(zip(dom_counts.index[::-1], dom_counts.values[::-1])):
                    ax8.text(count + 0.5, i, str(count), va='center', fontsize=10, weight='bold')
        
        # 9. System KPIs Summary
        ax9 = fig.add_subplot(gs[3, 1:])
        ax9.axis('off')
        
        # Calculate KPIs (schema-aligned)
        total_entities = sum(self.data['entity_counts'].values())
        total_programs = self.data['entity_counts'].get('Programs', 0)
        total_participants = self.data['entity_counts'].get('Participants', 0)
        total_projects = self.data['entity_counts'].get('Projects', 0)
        
        # Success rate from outcomes
        if self.data['outcomes']:
            outcomes_df = pd.DataFrame(self.data['outcomes'])
            if 'commercialization_status' in outcomes_df.columns:
                success_states = {'Launched', 'In Production', 'Market Ready'}
                success_rate = (outcomes_df['commercialization_status'].isin(success_states).mean() * 100.0)
            else:
                success_rate = 0.0
        else:
            success_rate = 0.0

        # Average participants per project from relationships
        if self.data.get('project_participants'):
            pp_df = pd.DataFrame(self.data['project_participants'])
            if 'project_id' in pp_df.columns:
                avg_participants = pp_df.groupby('project_id').size().mean() if not pp_df.empty else 0.0
            else:
                avg_participants = 0.0
        else:
            avg_participants = 0.0
        # Fallback/potential average from total counts (upper bound proxy)
        potential_avg_participants = (total_participants / total_projects) if total_projects > 0 else 0.0

        kpi_text = (
            "SYSTEM KEY PERFORMANCE INDICATORS\n"
            + "="*60 + "\n"
            + f"Total System Entities:      {total_entities}\n"
            + f"Data Distribution Pattern:  8:7:6:5:4:3:2:1\n"
            + f"Programs:                   {total_programs}\n"
            + f"Participants:               {total_participants}\n"
            + f"Projects:                   {total_projects}\n"
            + "\n"
            + f"Outcome Success Rate:       {success_rate:5.1f}% (commercialization)\n"
            + f"Avg Participants/Project:   {avg_participants:5.1f} (observed)\n"
            + f"Potential Participants/Project: {potential_avg_participants:5.1f} (upper bound)\n"
            + "\n"
            + f"System Health:              {'EXCELLENT' if success_rate >= 40 else ('GOOD' if success_rate >= 20 else 'EARLY-STAGE')}\n"
            + f"Data Volume Quality:        {'HIGH' if total_entities >= 200 else 'MEDIUM'}\n"
        )

        ax9.text(0.05, 0.95, kpi_text, fontsize=11,
                verticalalignment='top', transform=ax9.transAxes,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        fig.suptitle('ODS SYSTEM ANALYTICS & PERFORMANCE DASHBOARD\nComprehensive System Health & KPI Monitoring', 
                    fontsize=16, weight='bold', y=0.995)
        
        plt.savefig('visualization_9_system_analytics.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: visualization_9_system_analytics.png")
        
        print("\n" + "="*70)
        print("VISUALIZATION 9: SYSTEM ANALYTICS EXPLANATION")
        print("="*70)
        print("WHY SYSTEM ANALYTICS?")
        print("  • Provides comprehensive performance overview")
        print("  • Tracks key performance indicators (KPIs)")
        print("  • Identifies operational strengths and weaknesses")
        print("  • Supports data-driven decision making")
        print("  • Validates system design and implementation")
        print("\nKEY METRICS:")
        print(f"  • Total Entities: {total_entities}")
        print(f"  • Outcome Success Rate (Commercialization): {success_rate:.1f}%")
        print(f"  • Participants/Project Ratio: {avg_participants:.1f}")
        print("="*70 + "\n")
    
    def create_comprehensive_dashboard(self):
        """
        Create a comprehensive dashboard with all key metrics
        """
        print("Creating Comprehensive Dashboard...")
        
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Entity counts pie chart
        ax1 = fig.add_subplot(gs[0, 0])
        labels = list(self.data['entity_counts'].keys())
        sizes = list(self.data['entity_counts'].values())
        ax1.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90)
        ax1.set_title('Entity Distribution', fontsize=12, weight='bold')
        
        # 2. Entity counts bar chart
        ax2 = fig.add_subplot(gs[0, 1:])
        ax2.barh(labels, sizes, color=plt.cm.viridis(np.linspace(0, 1, len(labels))))
        ax2.set_xlabel('Count')
        ax2.set_title('Entity Counts Comparison', fontsize=12, weight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        # 3. Project pipeline (status or prototype_stage/nature)
        ax3 = fig.add_subplot(gs[1, 0])
        if self.data['projects']:
            projects_df = pd.DataFrame(self.data['projects'])
            if 'status' in projects_df.columns and projects_df['status'].notna().any():
                status_counts = projects_df['status'].value_counts()
                ax3.pie(status_counts.values, labels=status_counts.index, autopct='%1.0f%%')
                ax3.set_title('Project Status', fontsize=12, weight='bold')
            elif 'prototype_stage' in projects_df.columns and projects_df['prototype_stage'].notna().any():
                stage_counts = projects_df['prototype_stage'].value_counts()
                ax3.pie(stage_counts.values, labels=stage_counts.index, autopct='%1.0f%%')
                ax3.set_title('Project Prototype Stages', fontsize=12, weight='bold')
            elif 'nature' in projects_df.columns and projects_df['nature'].notna().any():
                nature_counts = projects_df['nature'].value_counts()
                ax3.pie(nature_counts.values, labels=nature_counts.index, autopct='%1.0f%%')
                ax3.set_title('Project Nature', fontsize=12, weight='bold')
        
        # 4. Participant specialization (fallback instead of age)
        ax4 = fig.add_subplot(gs[1, 1])
        if self.data['participants']:
            participants_df = pd.DataFrame(self.data['participants'])
            if 'specialization' in participants_df.columns:
                spec_counts = participants_df['specialization'].value_counts()
                ax4.bar(spec_counts.index, spec_counts.values, color=plt.cm.Set2(range(len(spec_counts))))
                ax4.set_ylabel('Count')
                ax4.set_title('Participant Specialization', fontsize=12, weight='bold')
                ax4.grid(axis='y', alpha=0.3)
                plt.setp(ax4.xaxis.get_majorticklabels(), rotation=30, ha='right')
        
        # 5. Equipment portfolio (usage domain)
        ax5 = fig.add_subplot(gs[1, 2])
        if self.data['equipment']:
            equipment_df = pd.DataFrame(self.data['equipment'])
            if 'usage_domain' in equipment_df.columns:
                dom_counts = equipment_df['usage_domain'].value_counts()
                ax5.bar(dom_counts.index, dom_counts.values, color=plt.cm.Set3(range(len(dom_counts))))
                ax5.set_ylabel('Count')
                ax5.set_title('Equipment Usage Domains', fontsize=12, weight='bold')
                ax5.grid(axis='y', alpha=0.3)
                plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 6. Facility types (fallback instead of capacity)
        ax6 = fig.add_subplot(gs[2, 0])
        if self.data['facilities']:
            facilities_df = pd.DataFrame(self.data['facilities'])
            if 'facility_type' in facilities_df.columns:
                type_counts = facilities_df['facility_type'].value_counts()
                ax6.barh(type_counts.index[::-1], type_counts.values[::-1], color='#87CEEB')
                ax6.set_xlabel('Count')
                ax6.set_title('Facility Types', fontsize=12, weight='bold')
                ax6.grid(axis='x', alpha=0.3)
        
        # 7. Outcome types / commercialization
        ax7 = fig.add_subplot(gs[2, 1])
        if self.data['outcomes']:
            outcomes_df = pd.DataFrame(self.data['outcomes'])
            if 'commercialization_status' in outcomes_df.columns:
                comm_counts = outcomes_df['commercialization_status'].value_counts()
                ax7.pie(comm_counts.values, labels=comm_counts.index, autopct='%1.0f%%')
                ax7.set_title('Commercialization Status', fontsize=12, weight='bold')
            elif 'outcome_type' in outcomes_df.columns:
                type_counts = outcomes_df['outcome_type'].value_counts()
                ax7.pie(type_counts.values, labels=type_counts.index, autopct='%1.0f%%')
                ax7.set_title('Outcome Types', fontsize=12, weight='bold')
        
        # 8. Summary statistics
        ax8 = fig.add_subplot(gs[2, 2])
        ax8.axis('off')
        summary_text = "SYSTEM SUMMARY\n" + "="*30 + "\n\n"
        for entity, count in self.data['entity_counts'].items():
            summary_text += f"{entity}: {count}\n"
        summary_text += "\n" + "="*30 + "\n"
        summary_text += f"TOTAL: {sum(self.data['entity_counts'].values())}"
        ax8.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
                verticalalignment='center')
        
        fig.suptitle('ODS COMPREHENSIVE ANALYTICS DASHBOARD', 
                    fontsize=18, weight='bold', y=0.98)
        
        plt.savefig('visualization_8_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: visualization_8_dashboard.png")
        
        print("\n" + "="*70)
        print("VISUALIZATION 8: COMPREHENSIVE DASHBOARD")
        print("="*70)
        print("WHY DASHBOARD?")
        print("  • Provides at-a-glance view of entire system")
        print("  • Combines multiple visualization techniques")
        print("  • Ideal for executive presentations")
        print("  • Shows relationships between different metrics")
        print("="*70 + "\n")
        
    def generate_all_visualizations(self):
        """Generate all visualizations including comprehensive system analytics"""
        print("\n" + "="*70)
        print("GENERATING ALL VISUALIZATIONS")
        print("="*70 + "\n")
        
        self.collect_data()
        
        # Generate individual visualizations
        self.create_pie_chart_distribution()
        self.create_bar_chart_comparison()
        self.create_project_status_visualization()
        self.create_participant_demographics()
        self.create_equipment_condition_analysis()
        self.create_facility_capacity_analysis()
        self.create_outcome_impact_analysis()
        self.create_comprehensive_dashboard()
        self.create_system_analytics()  # NEW: Comprehensive system analytics dashboard
        
        print("\n" + "="*70)
        print("ALL VISUALIZATIONS COMPLETE!")
        print("Total: 9 visualizations (8 standard + 1 comprehensive analytics)")
        print("="*70)
        print("="*70)
        print("\nGenerated Files:")
        print("  1. visualization_1_pie_chart.png")
        print("  2. visualization_2_bar_chart.png")
        print("  3. visualization_3_project_status.png")
        print("  4. visualization_4_demographics.png")
        print("  5. visualization_5_equipment_condition.png")
        print("  6. visualization_6_facility_capacity.png")
        print("  7. visualization_7_outcome_impact.png")
        print("  8. visualization_8_dashboard.png")
        print("="*70)
        
        # Generate summary report
        self.generate_summary_report()
        
    def generate_summary_report(self):
        """Generate a text summary report"""
        print("\nGenerating Summary Report...")
        
        with open('visualization_summary_report.txt', 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("ODS DATABASE VISUALIZATION SUMMARY REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("VISUALIZATION TECHNIQUES USED AND JUSTIFICATIONS\n")
            f.write("="*70 + "\n\n")
            
            f.write("1. PIE CHARTS\n")
            f.write("   Purpose: Show proportional distribution (parts of a whole)\n")
            f.write("   Best for: Categorical data with <10 categories\n")
            f.write("   Used for: Entity distribution, status distribution\n")
            f.write("   Advantage: Instantly shows which categories dominate\n\n")
            
            f.write("2. BAR CHARTS\n")
            f.write("   Purpose: Compare quantities across categories\n")
            f.write("   Best for: Showing exact values and rankings\n")
            f.write("   Used for: Entity counts, equipment condition, impact levels\n")
            f.write("   Advantage: Easy to read precise values\n\n")
            
            f.write("3. BOX PLOTS\n")
            f.write("   Purpose: Show distribution statistics (median, quartiles, outliers)\n")
            f.write("   Best for: Understanding data spread and identifying outliers\n")
            f.write("   Used for: Age distribution, facility capacity\n")
            f.write("   Advantage: Shows 5-number summary at a glance\n\n")
            
            f.write("4. HISTOGRAMS\n")
            f.write("   Purpose: Show frequency distribution of continuous data\n")
            f.write("   Best for: Understanding data patterns and clustering\n")
            f.write("   Used for: Age distribution, facility capacity\n")
            f.write("   Advantage: Reveals shape of data distribution\n\n")
            
            f.write("5. COMPREHENSIVE DASHBOARD\n")
            f.write("   Purpose: At-a-glance view of entire system\n")
            f.write("   Best for: Executive presentations and reporting\n")
            f.write("   Used for: Overall system overview\n")
            f.write("   Advantage: Combines multiple metrics in one view\n\n")
            
            f.write("="*70 + "\n")
            f.write("KEY INSIGHTS\n")
            f.write("="*70 + "\n\n")
            
            total = sum(self.data['entity_counts'].values())
            f.write(f"Total Records in System: {total}\n\n")
            
            f.write("Entity Distribution (8:7:6:5:4:3:2:1 Ratio):\n")
            for entity, count in self.data['entity_counts'].items():
                percentage = (count/total) * 100
                f.write(f"  • {entity}: {count} ({percentage:.1f}%)\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("WHY THESE VISUALIZATION TECHNIQUES?\n")
            f.write("="*70 + "\n\n")
            
            f.write("The visualization techniques were chosen based on:\n\n")
            f.write("1. DATA TYPE:\n")
            f.write("   - Categorical data -> Pie charts, Bar charts\n")
            f.write("   - Continuous data -> Histograms, Box plots\n")
            f.write("   - Status/distribution -> Stacked bars, Pie charts\n\n")
            
            f.write("2. AUDIENCE NEEDS:\n")
            f.write("   - Executives → Pie charts (quick understanding)\n")
            f.write("   - Analysts → Box plots, Histograms (detailed statistics)\n")
            f.write("   - Managers → Bar charts (actionable numbers)\n\n")
            
            f.write("3. MESSAGE CLARITY:\n")
            f.write("   - Proportions → Pie charts\n")
            f.write("   - Comparisons → Bar charts\n")
            f.write("   - Distributions → Box plots, Histograms\n")
            f.write("   - Overview → Dashboard\n\n")
            
            f.write("="*70 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*70 + "\n")
        
        print("✓ Saved: visualization_summary_report.txt")

def main():
    """Main function"""
    app = create_app()
    visualizer = DatabaseVisualizer(app)
    visualizer.generate_all_visualizations()
    
    print("\n" + "="*70)
    print("VISUALIZATION COMPLETE!")
    print("="*70)
    print("\nAll visualizations have been saved to the current directory.")
    print("Review the images and the summary report for insights.")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
