from api.models import Service, db
from sqlalchemy.orm import sessionmaker

list = []
class seed: 
    def __init__(self, name, duration): 
        self.name = name 
        self.duration = duration

list.append(seed(name="Car service", duration=200))
list.append(seed(name="Home service", duration=300))
list.append(seed(name="Dental service", duration=100))

if __name__  ==  "__main__" :
    for seed in list:
        seed = Service(name = seed.name, duration = seed.duration)
        db.session.add(seed)
        db.session.commit()
