
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import models
import schemas

# --- Topic CRUD ---

def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).filter(models.Topic.id == topic_id).first()

def get_topics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Topic).offset(skip).limit(limit).all()

def create_topic(db: Session, topic: schemas.TopicCreate):
    db_topic = models.Topic(
        name=topic.name,
        keywords=topic.keywords,
        # Settings
        frequency=topic.settings.frequency,
        custom_date_range=topic.settings.custom_date_range,
        detection_time=topic.settings.detection_time,
        notification_channels=topic.settings.notification_channels,
        # PPT Settings
        template=topic.ppt_settings.template,
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def update_topic(db: Session, topic_id: int, topic_update: schemas.TopicCreate):
    db_topic = get_topic(db, topic_id)
    if not db_topic:
        return None

    update_data = topic_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "settings":
            for s_key, s_value in value.items():
                setattr(db_topic, s_key, s_value)
        elif key == "ppt_settings":
            for p_key, p_value in value.items():
                setattr(db_topic, p_key, p_value)
        else:
            setattr(db_topic, key, value)

    db_topic.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(db_topic)
    return db_topic

def delete_topic(db: Session, topic_id: int):
    db_topic = get_topic(db, topic_id)
    if db_topic:
        db.delete(db_topic)
        db.commit()
        return True
    return False

def get_topic_history(db: Session, topic_id: int):
    return db.query(models.UpdateRecord).filter(models.UpdateRecord.topic_id == topic_id).all()


# --- Literature CRUD ---

def create_literature(db: Session, literature: schemas.Literature, topic_id: int):
    db_literature = models.Literature(**literature.dict(), topic_id=topic_id)
    db.add(db_literature)
    db.commit()
    db.refresh(db_literature)
    return db_literature

def get_literature_analysis(db: Session, topic_id: int, skip: int = 0, limit: int = 10):
    base_query = db.query(models.Literature).filter(models.Literature.topic_id == topic_id)

    # Stats
    total_count = base_query.count()
    # Assuming high citation is > 50, a real implementation would be more complex
    # For now, we will return a placeholder value for high_citation_count
    high_citation_count = 0 # Placeholder
    clinical_trial_count = base_query.filter(models.Literature.literature_type.ilike("%clinical trial%")).count()
    meta_analysis_count = base_query.filter(models.Literature.literature_type.ilike("%meta-analysis%")).count()

    stats = schemas.LiteratureAnalysisStats(
        total_count=total_count,
        high_citation_count=high_citation_count,
        clinical_trial_count=clinical_trial_count,
        meta_analysis_count=meta_analysis_count
    )

    # Trend Data (e.g., last 6 months)
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    trend_data_query = (((db.query(
            func.strftime('%Y-%m', models.Literature.publication_date).label('month'),
            func.count(models.Literature.id).label('count')
        ).filter(models.Literature.topic_id == topic_id)
                        .filter(models.Literature.publication_date >= six_months_ago)
                        .group_by(func.strftime('%Y-%m', models.Literature.publication_date)))
                        .order_by(func.strftime('%Y-%m', models.Literature.publication_date)))
                        .all())
    
    trend_data = [schemas.TrendDataPoint(date=row.month, count=row.count) for row in trend_data_query]

    # Distribution Data
    distribution_query = ((db.query(
            models.Literature.literature_type,
            func.count(models.Literature.id).label('count')
        ).filter(models.Literature.topic_id == topic_id)
                          .group_by(models.Literature.literature_type))
                          .all())

    distribution_data = [schemas.DistributionDataPoint(type=row.literature_type, count=row.count) for row in distribution_query]

    # Literature List
    literature_list = base_query.order_by(models.Literature.publication_date.desc()).offset(skip).limit(limit).all()

    return schemas.LiteratureAnalysis(
        stats=stats,
        trend_data=trend_data,
        distribution_data=distribution_data,
        literature=literature_list
    )


# --- PPT Push History CRUD ---

def get_ppt_push_history(db: Session, skip: int = 0, limit: int = 100):
    results = (
        db.query(models.PPTPushRecord, models.PPTDiff.summary)
        .outerjoin(models.PPTDiff, models.PPTPushRecord.id == models.PPTDiff.current_record_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    history_records = []
    for record, diff_summary in results:
        record_dict = record.__dict__
        record_dict['diff_summary'] = diff_summary
        history_records.append(schemas.PPTPushRecord.model_validate(record_dict))
        
    return history_records
