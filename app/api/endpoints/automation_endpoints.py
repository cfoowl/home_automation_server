
from sqlalchemy.orm import Session
from app.models.automation import Automation

def delete_automation_by_id_endpoint(db: Session, automation_id: int):
    automation = db.query(Automation).filter(Automation.id == automation_id).first()
    db.delete(automation)
    db.commit()
    return {"message": "Automation deleted successfully"}


def get_all_automations_endpoint(db: Session):
    return db.query(Automation).all()

def get_automation_by_id_endpoint(db: Session, automation_id: int):
    return db.query(Automation).filter(Automation.id == automation_id).first()

def create_automation_endpoint(db: Session, sensor_id: int, sensor_type: str, condition_type: str, condition_operator: str, condition_value, actuator_id: int, action_id: int):
    condition = {
        "type" : condition_type,
        "operator" : condition_operator,
        "value" : condition_value
    }
    new_automation = Automation(sensor_id=sensor_id, sensor_type=sensor_type, condition=condition, actuator_id=actuator_id, action_id=action_id)
    
    db.add(new_automation)
    db.commit()
    db.refresh(new_automation)
    return {"id" : new_automation.id}
