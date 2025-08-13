import logging
from datetime import time, datetime, timedelta
from sqlalchemy.orm import Session
import random
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import necessary components from your project
import crud
import schemas
from models import Base, Topic, UpdateRecord, Literature, PPTPushRecord, PPTDiff
from database import SessionLocal, engine

def clear_database():
    """
    Drops all tables and recreates them. This will delete all existing data.
    """
    logger.info("Clearing database: dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("Recreating all tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database cleared and tables recreated successfully.")

def insert_test_data(db: Session):
    """
    Inserts a predefined set of realistic test data into the database for
    the "Chronic Lymphocytic Leukemia (Quarterly)" theme.
    """
    logger.info("Inserting test data...")

    # 1. Create Topic: Chronic Lymphocytic Leukemia (CLL)
    logger.info("Creating the main topic...")
    cll_topic_data = schemas.TopicCreate(
        name="慢性淋巴细胞白血病 (每季度)",
        keywords=["CLL", "Ibrutinib", "Venetoclax", "BTK inhibitors", "Minimal Residual Disease"],
        frequency="quarterly",
        detection_time=time(10, 0, 0),
        notification_channels=["email", "app_push"],
        template="modern_blue"
    )
    
    topic = crud.create_topic(db=db, topic=cll_topic_data)
    logger.info(f"Topic '{topic.name}' created successfully with ID {topic.id}.")

    # 2. Create Literature for the past quarters
    logger.info("Inserting sample literature for CLL...")
    # 真实数据替换版
    logger.info("Inserting real literature data for CLL...")
    Q1 = [
        {
            "title": "Chronic Lymphocytic Leukemia: 2025 Update on the Epidemiology, Pathogenesis, Diagnosis, and Therapy",
            "authors": ["Hallek, M.", "Al-Sawaf, O."],
            "publication_date": datetime(2025, 1, 28),
            "journal": "American Journal of Hematology",
            "keywords": ["CLL", "Epidemiology", "Pathogenesis", "Therapy"],
            "summary": "In the most recent update of the SEER database, the age-adjusted incidence of chronic lymphocytic leukemia (CLL) was 4.6 per 100 000 inhabitants. Combinations of targeted agents now provide efficient therapies with a fixed duration that generate deep and durable remissions. The paper reviews epidemiology, pathogenesis, diagnosis, and evolving treatments.",
            "literature_type": "Review"
        },
        {
            "title": "Upfront fixed-duration treatment strategies for chronic lymphocytic leukemia in Arab populations: a position statement from the Gulf region",
            "authors": ["Yassin, M. A.", "Al Farsi, K.", "Hamad, A.", "Ghasoub, R.", "Alhuraiji, A.", "Mheidly, K.",
                        "Aal Yaseen, H.", "Osman, H.", "Trepel, M."],
            "publication_date": datetime(2025, 2, 26),
            "journal": "Frontiers in Medicine",
            "keywords": ["Chronic lymphocytic leukemia", "Fixed-duration treatment", "Ibrutinib", "Venetoclax",
                         "Obinutuzumab", "Arab", "Middle East"],
            "summary": "Chronic lymphocytic leukemia (CLL) treatment has evolved with various effective options, but management in Arab patients, who are typically younger and have comorbidities like diabetes and obesity, requires specific considerations due to the lack of regional guidelines. Experts recommend ibrutinib-venetoclax as the first-line therapy for all fit CLL patients, reviewing clinical data from trials like CAPTIVATE and GLOW.",
            "literature_type": "Review"
        },
        {
            "title": "What's New in Chronic Lymphocytic Leukemia (CLL) Research?",
            "authors": ["American Cancer Society Research Team"],
            "publication_date": datetime(2025, 3, 20),
            "journal": "American Cancer Society Journal",
            "keywords": ["CLL Research", "Prevention", "Treatment Advances"],
            "summary": "Research into causes, prevention, and treatment of CLL is ongoing in many medical centers throughout the world. This update covers new developments in targeted therapies, immunotherapies, and early detection methods.",
            "literature_type": "Review"
        },
    {
        "title": "Fixed-Duration Acalabrutinib Combinations in Untreated Chronic Lymphocytic Leukemia",
        "authors": ["Brown, J. R.", "Sharman, J. P."],
        "publication_date": datetime(2025, 2, 20),
        "journal": "New England Journal of Medicine",
        "keywords": ["Acalabrutinib", "Fixed-Duration Therapy", "CLL", "Phase 3 Trial"],
        "summary": "This Phase 3 trial evaluated fixed-duration acalabrutinib combinations in untreated CLL patients, demonstrating significant efficacy and manageable safety profile.",
        "literature_type": "Clinical Trial"
    },
    {
        "title": "Chronic Lymphocytic Leukemia Care and Beyond",
        "authors": ["Al-Sawaf, O.", "Hallek, M."],
        "publication_date": datetime(2025, 1, 2),
        "journal": "Cancers (Basel)",
        "keywords": ["CLL", "Management", "Therapy Advances", "Review"],
        "summary": "A comprehensive review of CLL care, covering epidemiology, novel therapeutic strategies, and emerging challenges in management.",
        "literature_type": "Review"
    },
    {
        "title": "Is MRD testing ready for general use in CLL?",
        "authors": ["Owen, C."],
        "publication_date": datetime(2025, 1, 31),
        "journal": "Clinical Advances in Hematology & Oncology",
        "keywords": ["Minimal Residual Disease", "MRD", "Diagnostics", "CLL"],
        "summary": "Review discussing current MRD detection methods in CLL and their clinical applicability for guiding therapy.",
        "literature_type": "Review"
    },
    {
        "title": "Highlights in CLL from the 66th ASH",
        "authors": ["Wierda, W. G."],
        "publication_date": datetime(2025, 2, 1),
        "journal": "Clinical Advances in Hematology & Oncology (Suppl.)",
        "keywords": ["CLL", "ASH 2024 Highlights", "Clinical Trials", "Research Updates"],
        "summary": "Summary of key CLL research and clinical trial updates presented at the 66th ASH meeting.",
        "literature_type": "Review"
    },
    {
        "title": "ELEVATE-TN: 4-year follow-up correspondence",
        "authors": ["Sharman, J. P."],
        "publication_date": datetime(2025, 2, 1),
        "journal": "Leukemia",
        "keywords": ["Acalabrutinib", "CLL", "Long-term Follow-up", "ELEVATE-TN Trial"],
        "summary": "Follow-up correspondence reporting four-year outcomes of the ELEVATE-TN trial evaluating acalabrutinib in treatment-naïve CLL.",
        "literature_type": "Letter"
    },
    {
        "title": "CLL often arises by a multiclonal selection process",
        "authors": ["Bagnara, D."],
        "publication_date": datetime(2025, 2, 20),
        "journal": "Haematologica",
        "keywords": ["CLL", "Clonal Evolution", "Genomics", "Pathogenesis"],
        "summary": "Study exploring the multiclonal origins of CLL, highlighting the complexity of tumor heterogeneity in disease progression.",
        "literature_type": "Mechanistic Study"
    },
    {
        "title": "Real-world outcomes with ibrutinib monotherapy in CLL",
        "authors": ["Smith, A."],
        "publication_date": datetime(2025, 1, 1),
        "journal": "Oncology in Clinical Practice",
        "keywords": ["Ibrutinib", "CLL", "Real-World Data", "Monotherapy"],
        "summary": "Analysis of treatment outcomes and safety of ibrutinib monotherapy in a real-world cohort of CLL patients.",
        "literature_type": "Real-world Study"
    },
    {
        "title": "Fixed-dose regimens in CLL",
        "authors": ["Kater, A."],
        "publication_date": datetime(2025, 3, 1),
        "journal": "Clinical Advances in Hematology & Oncology",
        "keywords": ["CLL", "Fixed-Dose Therapy", "Treatment Regimens", "Review"],
        "summary": "Review covering fixed-dose treatment regimens in CLL, their rationale, and clinical outcomes.",
        "literature_type": "Review"
    },
    {
        "title": "Survival & Prognostic Factors with Drug-Related Remission in CLL",
        "authors": ["Pektaş, G."],
        "publication_date": datetime(2025, 3, 14),
        "journal": "Diagnostics (Basel)",
        "keywords": ["CLL", "Prognosis", "Survival", "Remission"],
        "summary": "Retrospective study identifying factors associated with long-term survival and remission in drug-treated CLL patients.",
        "literature_type": "Retrospective Study"
    },
    {
        "title": "Clinical trial participation & outcomes by practice setting (CLL/MCL)",
        "authors": ["Bruno, D. S."],
        "publication_date": datetime(2025, 2, 5),
        "journal": "Hematology",
        "keywords": ["Clinical Trials", "Practice Settings", "CLL", "Mantle Cell Lymphoma"],
        "summary": "Investigation of patient outcomes in CLL and MCL based on clinical trial participation across different healthcare settings.",
        "literature_type": "Database Study"
    }
    ]
    Q2 = [
        {
        "title": "When and How Long to Treat Chronic Lymphocytic Leukemia?",
        "authors": ["Eichhorst, B.", "Goede, V."],
        "publication_date": datetime(2025, 4, 24),
        "journal": "Journal of Clinical Oncology",
        "keywords": ["CLL Treatment Duration", "Allogeneic Transplant", "Targeted Therapy"],
        "summary": "Chronic lymphocytic leukemia (CLL) remains an incurable disease, except in rare cases treated with allogeneic stem-cell transplantation or favorable-risk CLL. This paper discusses optimal timing and duration of therapies, including BTK inhibitors and BCL-2 antagonists.",
        "literature_type": "Review"
    },
    {
        "title": "Optimizing disease risk stratification and clinical outcomes in chronic lymphocytic leukemia",
        "authors": ["Bartkowiak, M.", "Hoechstetter, M."],
        "publication_date": datetime(2025, 5, 21),
        "journal": "Magazine of European Medical Oncology",
        "keywords": ["CLL", "Prognostic Tools", "Targeted Agents"],
        "summary": "This article discusses three key topics in CLL with novel clinical trial data, addressing management strategies for early-stage patients, treatment for frail patients, and shifting from indefinite monotherapy to time-limited combinations.",
        "literature_type": "Review"
    },
    {
        "title": "Measurable Residual Disease–Guided Therapy for Chronic Lymphocytic Leukemia",
        "authors": ["Munir, T.", "Girvan, S.", "Cairns, D. A.", "Bloor, A.", "Allsup, D.", "Varghese, A. M.", "Gohil, S.", "Paneesha, S.", "Pettitt, A.", "Eyre, T.", "Fox, C. P.", "Forconi, F.", "Balotis, C.", "Pemberton, N.", "Sheehy, O.", "Gribben, J.", "Elmusharaf, N.", "Gatto, S.", "Preston, G.", "Schuh, A.", "Walewska, R.", "Duley, L.", "Webster, N.", "Dalal, S.", "Rawstron, A.", "Howard, D.", "Hockaday, A.", "Jackson, S.", "Greatorex, N.", "Bell, S.", "Stones, D.", "Brown, J. M.", "Patten, P. E. M.", "Hillmen, P."],
        "publication_date": datetime(2025, 6, 15),
        "journal": "New England Journal of Medicine",
        "keywords": ["MRD-Guided Therapy", "Progression-Free Survival", "CLL"],
        "summary": "With extended follow-up, the trial showed that undetectable MRD and extended progression-free survival were more common with ibrutinib–venetoclax than with ibrutinib alone or FCR.",
        "literature_type": "Clinical Trial"
    },
        {
            "title": "Measurable Residual Disease–Guided Therapy for Chronic Lymphocytic Leukemia",
            "authors": ["Munir, T.", "Girvan, S."],
            "publication_date": datetime(2025, 6, 16),
            "journal": "New England Journal of Medicine",
            "keywords": ["MRD-Guided Therapy", "Progression-Free Survival", "CLL", "Clinical Trial"],
            "summary": "The trial showed undetectable MRD and improved progression-free survival with ibrutinib–venetoclax versus ibrutinib alone or FCR in CLL.",
            "literature_type": "Clinical Trial"
        },
        {
            "title": "When and How Long to Treat Chronic Lymphocytic Leukemia?",
            "authors": ["Eichhorst, B.", "Goede, V."],
            "publication_date": datetime(2025, 4, 24),
            "journal": "Journal of Clinical Oncology",
            "keywords": ["CLL", "Treatment Duration", "BTK Inhibitors", "BCL-2 Antagonists"],
            "summary": "Review discussing optimal timing and duration of therapies in CLL, including the role of targeted agents and transplant.",
            "literature_type": "Review"
        },
        {
            "title": "Double-refractory Chronic Lymphocytic Leukemia: New Deal in Clinical Management",
            "authors": ["Bennett, R.", "Seymour, J. F."],
            "publication_date": datetime(2025, 4, 10),
            "journal": "Blood",
            "keywords": ["Double-Refractory CLL", "BTK Inhibitors", "Pirtobrutinib", "CAR-T Therapy"],
            "summary": "Review of treatment strategies for double-refractory CLL, including novel agents and immunotherapies.",
            "literature_type": "Review"
        },
        {
            "title": "T cells in B-cell Chronic Lymphocytic Leukemia: Bystanders or Partners in Crime?",
            "authors": ["Stokłosa, T."],
            "publication_date": datetime(2025, 4, 24),
            "journal": "Polish Archives of Internal Medicine",
            "keywords": ["T cells", "CLL", "Immune Microenvironment", "Review"],
            "summary": "Analysis of the role of T cells in CLL pathogenesis and their potential as therapeutic targets.",
            "literature_type": "Review"
        },
        {
            "title": "Cardiac Events Across Three Acalabrutinib Phase 3 Trials in Chronic Lymphocytic Leukemia",
            "authors": ["O'Quinn, R."],
            "publication_date": datetime(2025, 4, 30),
            "journal": "Clinical Lymphoma Myeloma and Leukemia",
            "keywords": ["Cardiac Events", "Acalabrutinib", "Safety", "CLL"],
            "summary": "Meta-analysis of cardiac adverse events in CLL patients treated with acalabrutinib in Phase 3 trials.",
            "literature_type": "Meta-analysis"
        },
        {
            "title": "CLL Cell-Derived Exosomes Alter Immune and Hematopoietic Compartments",
            "authors": ["Martínez, P."],
            "publication_date": datetime(2025, 4, 1),
            "journal": "Haematologica",
            "keywords": ["Exosomes", "Immune Modulation", "CLL", "Mechanistic Study"],
            "summary": "Study demonstrating how CLL-derived exosomes impact immune function and hematopoiesis.",
            "literature_type": "Mechanistic Study"
        },
        {
            "title": "GELLC Guidelines for Diagnosis and Treatment of Chronic Lymphocytic Leukemia",
            "authors": ["GELLC Working Group"],
            "publication_date": datetime(2025, 4, 1),
            "journal": "Medicina Clínica (Barc)",
            "keywords": ["Guidelines", "CLL", "Diagnosis", "Treatment"],
            "summary": "Official Spanish guidelines on diagnosis and management of CLL patients.",
            "literature_type": "Guideline"
        },
        {
            "title": "Outcomes After Discontinuation of Covalent BTK Inhibitors in CLL",
            "authors": ["Rodríguez, L."],
            "publication_date": datetime(2025, 5, 1),
            "journal": "Leukemia & Lymphoma",
            "keywords": ["BTK Inhibitors", "Discontinuation", "CLL", "Real-World Outcomes"],
            "summary": "Real-world analysis of patient outcomes following cessation of covalent BTKi therapy in CLL.",
            "literature_type": "Real-world Study"
        },
        {
            "title": "Fixed-Duration Acalabrutinib Combinations: Trial Methodology and Supplemental Data",
            "authors": ["Brown, J. R."],
            "publication_date": datetime(2025, 2, 5),
            "journal": "New England Journal of Medicine (Supplement)",
            "keywords": ["Acalabrutinib", "Fixed-Duration", "Clinical Trial", "Supplemental Data"],
            "summary": "Supplemental material detailing methodology and additional results for the acalabrutinib fixed-duration trial.",
            "literature_type": "Supplemental Data"
        },
        {
            "title": "Optimizing Disease Risk Stratification and Clinical Outcomes in Chronic Lymphocytic Leukemia",
            "authors": ["Bartkowiak, M.", "Hoechstetter, M."],
            "publication_date": datetime(2025, 5, 21),
            "journal": "Magazine of European Medical Oncology",
            "keywords": ["CLL", "Risk Stratification", "Targeted Therapy", "Clinical Outcomes"],
            "summary": "Review addressing prognostic tools and management strategies for diverse CLL patient populations.",
            "literature_type": "Review"
        }
    ]
    Q3 = [
    {
        "title": "Doubling down: the new deal in the clinical management of double-refractory chronic lymphocytic leukemia",
        "authors": ["Bennett, R.", "Seymour, J. F."],
        "publication_date": datetime(2025, 7, 10),
        "journal": "Blood",
        "keywords": ["Double-Refractory CLL", "BTK Inhibitors", "Clinical Management"],
        "summary": "Targeted therapy with covalent BTK inhibitors and venetoclax is established in CLL, but double-refractory disease poses challenges. The review discusses pirtobrutinib, CD19 CAR-T, and emerging therapies.",
        "literature_type": "Review"
    },
    {
        "title": "Fixed-Duration Ibrutinib/Venetoclax Shows Durable Responses in CLL, Says Dr Ghia",
        "authors": ["Ghia, P."],
        "publication_date": datetime(2025, 7, 11),
        "journal": "Targeted Oncology",
        "keywords": ["Ibrutinib", "Venetoclax", "Fixed-Duration", "IGHV Mutated"],
        "summary": "New findings reveal that fixed-duration ibrutinib plus venetoclax offers long-term efficacy and safety. 73% of patients remained treatment-free 5.5 years after therapy, with MRD status predicting outcomes.",
        "literature_type": "Clinical Trial"
    },
    {
        "title": "CLL Highlights from EHA 2025: Expert Perspectives and Clinical Developments",
        "authors": ["Wendtner, C."],
        "publication_date": datetime(2025, 7, 24),
        "journal": "EMJ Hematology",
        "keywords": ["BCL2 inhibitor", "BTK inhibitor", "CAR-T cell therapy", "CLL", "Continuous therapy", "First-line", "Fixed duration", "MRD"],
        "summary": "This article captures key research highlights from EHA 2025 on CLL, focusing on first-line management, therapeutic advances, biomarkers, and new directions like CAR-T and MRD-guided strategies.",
        "literature_type": "Review"
    },
        {
            "title": "Doubling Down: The New Deal in the Clinical Management of Double-Refractory Chronic Lymphocytic Leukemia",
            "authors": ["Bennett, R.", "Seymour, J. F."],
            "publication_date": datetime(2025, 7, 10),
            "journal": "Blood",
            "keywords": ["Double-Refractory CLL", "BTK Inhibitors", "Clinical Management", "Pirtobrutinib"],
            "summary": "Review discussing novel treatment approaches including pirtobrutinib and CAR-T therapies for double-refractory CLL.",
            "literature_type": "Review"
        },
        {
            "title": "Fixed-Duration Ibrutinib/Venetoclax Shows Durable Responses in CLL, Says Dr Ghia",
            "authors": ["Ghia, P."],
            "publication_date": datetime(2025, 7, 11),
            "journal": "Targeted Oncology",
            "keywords": ["Ibrutinib", "Venetoclax", "Fixed-Duration", "CLL"],
            "summary": "Clinical data showing durable responses and safety of fixed-duration ibrutinib plus venetoclax in CLL patients.",
            "literature_type": "Clinical Trial"
        },
        {
            "title": "CLL Highlights from EHA 2025: Expert Perspectives and Clinical Developments",
            "authors": ["Wendtner, C."],
            "publication_date": datetime(2025, 7, 24),
            "journal": "EMJ Hematology",
            "keywords": ["CLL", "EHA 2025", "BCL2 Inhibitors", "CAR-T", "MRD"],
            "summary": "Summary of research highlights from EHA 2025 covering novel therapeutics and emerging management strategies in CLL.",
            "literature_type": "Review"
        },
        {
            "title": "Management of Relapsed/Refractory Chronic Lymphocytic Leukemia",
            "authors": ["Kagerer, A."],
            "publication_date": datetime(2025, 7, 16),
            "journal": "Hematology/Oncology Clinics of North America",
            "keywords": ["Relapsed CLL", "Refractory CLL", "Management", "Therapies"],
            "summary": "Review focusing on therapeutic options and management strategies for relapsed/refractory CLL patients.",
            "literature_type": "Review"
        },
        {
            "title": "BRUIN CLL-321: Pirtobrutinib vs Idelalisib/Rituximab ± Ofatumumab in Relapsed/Refractory CLL",
            "authors": ["Tam, C. S."],
            "publication_date": datetime(2025, 7, 29),
            "journal": "Journal of Clinical Oncology",
            "keywords": ["Pirtobrutinib", "Idelalisib", "Rituximab", "Relapsed CLL", "Phase 3 Trial"],
            "summary": "Randomized Phase 3 trial comparing pirtobrutinib to standard therapies in relapsed/refractory CLL patients.",
            "literature_type": "Clinical Trial"
        },
        {
            "title": "International Consensus Recommendations on Richter Transformation",
            "authors": ["Expert Panel"],
            "publication_date": datetime(2025, 7, 17),
            "journal": "Blood",
            "keywords": ["Richter Transformation", "Consensus", "Diagnosis", "Management"],
            "summary": "Consensus recommendations on diagnosis, evaluation, and management of Richter transformation in CLL.",
            "literature_type": "Consensus Statement"
        },
        {
            "title": "Toggle Genes Driving Proliferation in Chronic Lymphocytic Leukemia",
            "authors": ["Sirbu, O."],
            "publication_date": datetime(2025, 8, 11),
            "journal": "NPJ Systems Biology and Applications",
            "keywords": ["CLL", "Gene Regulation", "Proliferation", "Systems Biology"],
            "summary": "Systems biology study identifying key toggle genes regulating CLL cell proliferation.",
            "literature_type": "Mechanistic Study"
        },
        {
            "title": "Inhibition of NEDDylation Enhances Cytostasis of Rohinitib in CLL Cells",
            "authors": ["Castaño, J. L."],
            "publication_date": datetime(2025, 8, 4),
            "journal": "Biomedicine & Pharmacotherapy",
            "keywords": ["NEDDylation", "Rohinitib", "CLL", "Preclinical Study"],
            "summary": "Preclinical research demonstrating enhanced cytostatic effects of Rohinitib on CLL cells via NEDDylation inhibition.",
            "literature_type": "Preclinical Study"
        },
        {
            "title": "Systematic Literature Review of Cardiovascular Safety Outcomes in Chronic Lymphocytic Leukemia Therapies",
            "authors": ["Johnson, A."],
            "publication_date": datetime(2025, 8, 4),
            "journal": "Journal of Cardio-Oncology",
            "keywords": ["Cardiovascular Safety", "CLL", "Therapies", "Systematic Review"],
            "summary": "Systematic review evaluating cardiovascular risks associated with current CLL therapeutic regimens.",
            "literature_type": "Systematic Review"
        },
        {
            "title": "Immunoglobulin Use, Survival, and Infections in Chronic Lymphocytic Leukemia",
            "authors": ["Martínez, P."],
            "publication_date": datetime(2025, 7, 25),
            "journal": "Leukemia & Lymphoma",
            "keywords": ["Immunoglobulin Therapy", "Survival", "Infections", "CLL"],
            "summary": "Real-world data analysis on immunoglobulin replacement therapy effects on survival and infection rates in CLL.",
            "literature_type": "Real-world Study"
        }
    ]
    literature_to_create = Q1 + Q2 +Q3

    for lit in literature_to_create:
        lit_data = Literature(
            topic_id=topic.id,
            title=lit["title"],
            authors=lit["authors"],
            publication_date=lit["publication_date"],
            journal_name=lit["journal"],
            keywords=lit["keywords"],
            summary=lit["summary"],
            literature_type=lit["literature_type"]
        )
        db.add(lit_data)

    db.commit()
    logger.info(f"{len(literature_to_create)} literature records inserted.")

    # 3. Create Update Records for past quarters
    logger.info("Inserting update history records...")
    update_records_to_create = [
        {"timestamp": datetime(2025, 3, 28), "status": "success", "ppt_link": "/PPT/慢性淋巴细胞白血病最新研究进展_1-3月.pptx"},
        {"timestamp": datetime(2025, 6, 28), "status": "success", "ppt_link": "/PPT/慢性淋巴细胞白血病最新研究进展_4-6月.pptx"},
    ]
    
    for record_data in update_records_to_create:
        update_record = UpdateRecord(
            topic_id=topic.id,
            timestamp=record_data["timestamp"],
            status=record_data["status"],
            ppt_preview_link=record_data["ppt_link"]
        )
        db.add(update_record)
    db.commit()
    logger.info(f"{len(update_records_to_create)} update records inserted.")

    # 4. Create PPT Push Records for successful updates
    logger.info("Inserting PPT push records...")
    recipients_pool = [
        json.dumps(["oncology_dept_head@medbrief.com", "research_lead@medbrief.com"]),
        json.dumps(["medical_affairs@pharma.com"]),
        json.dumps(["clinical_trials_group@medbrief.com"]),
    ]
    
    successful_updates = db.query(UpdateRecord).filter_by(topic_id=topic.id, status="success").all()
    
    for update in successful_updates:
        push_record = PPTPushRecord(
            push_time=update.timestamp + timedelta(minutes=15),
            topic_name=topic.name,
            ppt_filename=update.ppt_preview_link.split('/')[-1],
            recipients=random.choice(recipients_pool),
            channel=random.choice(["Email", "Webhook"]),
            status="success"
        )
        db.add(push_record)
    db.commit()
    logger.info(f"{len(successful_updates)} PPT push records inserted.")

    # 5. Create PPT Diffs
    logger.info("Creating PPT diff records...")
    # Get all PPT push records, grouped by topic and sorted by push_time
    all_ppt_records = db.query(PPTPushRecord).order_by(PPTPushRecord.topic_name, PPTPushRecord.push_time).all()
    
    records_by_topic = {}
    for record in all_ppt_records:
        if record.topic_name not in records_by_topic:
            records_by_topic[record.topic_name] = []
        records_by_topic[record.topic_name].append(record)

    for topic_name, records_list in records_by_topic.items():
        # Ensure records are sorted by push_time for correct diffing
        records_list.sort(key=lambda x: x.push_time)
        
        for i in range(1, len(records_list)):
            previous_record = records_list[i-1]
            current_record = records_list[i]
            
            # Generate a placeholder summary for the diff
            summary = """1-3月份的研究主要聚焦于CLL的分子机制、诊断管理和治疗前沿，强调BCR信号通路、IGHV与TP53遗传变异以及非编码RNA在耐药中的作用，治疗方面突出BTK与BCL-2抑制剂的突破和挑战，并探讨固定疗程与非共价BTKi，同时关注真实世界与临床试验的差异、中国与国际在患者管理和生存上的不同，以及AI和多组学在分层与智能决策中的应用与数据融合难题；4-6月份的研究则更深入探讨CLL的发病机制、分子风险分层和靶向免疫治疗，涵盖IGHV、TP53、ATM等核心标志物及HGF/c-MET、ROR1等新通路，治疗策略上强调BTK/BCL-2联合与固定疗程，并引入双特异抗体与CAR-T等未来趋势，真实世界数据方面关注中欧美患者特征和治疗模式差异及药物经济学与支付模式优化，同时着重于AI驱动的多组学治疗优化以及远程医疗与个体化管理的新方向。"""
            ppt_diff = PPTDiff(
                current_record_id=current_record.id,
                previous_record_id=previous_record.id,
                summary=summary
            )
            db.add(ppt_diff)
    db.commit()
    logger.info("PPT diff records created successfully.")


if __name__ == "__main__":
    logger.info("Starting database initialization script.")
    db_session = SessionLocal()
    try:
        clear_database()
        insert_test_data(db_session)
        logger.info("Script finished successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        db_session.close()
        logger.info("Database session closed.")