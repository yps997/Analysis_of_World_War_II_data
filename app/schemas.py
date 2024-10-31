import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import DateTime
from .models import Country, City, TargetType, Target, Mission
from .database import Session
from datetime import datetime

class CountryObject(SQLAlchemyObjectType):
    class Meta:
        model = Country

class CityObject(SQLAlchemyObjectType):
    class Meta:
        model = City

class TargetTypeObject(SQLAlchemyObjectType):
    class Meta:
        model = TargetType

class TargetObject(SQLAlchemyObjectType):
    class Meta:
        model = Target

class MissionObject(SQLAlchemyObjectType):
    class Meta:
        model = Mission

class Query(graphene.ObjectType):
    all_missions = graphene.List(MissionObject)
    mission_by_id = graphene.Field(MissionObject, mission_id=graphene.Int(required=True))
    missions_by_date_range = graphene.List(MissionObject, start_date=graphene.Date(required=True),end_date=graphene.Date(required=True))
    missions_by_country = graphene.List(MissionObject, country_name=graphene.String(required=True))
    missions_by_target_industry = graphene.List(MissionObject, industry=graphene.String(required=True))
    aircraft_by_mission = graphene.Field(MissionObject, mission_id=graphene.Int(required=True))
    attack_results_by_mission = graphene.Field(MissionObject,mission_id=graphene.Int(required=True))

    def resolve_all_missions(self, info):
        session = Session()
        try:
            return session.query(Mission).all()
        finally:
            session.close()

    def resolve_mission_by_id(self, info, mission_id):
        session = Session()
        try:
            return session.query(Mission).filter(Mission.mission_id == mission_id).first()
        finally:
            session.close()

    def resolve_missions_by_date_range(self, info, start_date, end_date):
        session = Session()
        try:
            return session.query(Mission).filter(
                Mission.mission_date.between(start_date, end_date)
            ).all()
        finally:
            session.close()

    def resolve_missions_by_country(self, info, country_name):
        session = Session()
        try:
            return session.query(Mission).join(Target).join(City).join(Country).filter(
                Country.country_name == country_name
            ).all()
        finally:
            session.close()

    def resolve_aircraft_by_mission(self, info, mission_id):
        session = Session()
        try:
            return session.query(Mission).filter(Mission.mission_id == mission_id).first()
        finally:
            session.close()

    def resolve_attack_results_by_mission(self, info, mission_id):
        session = Session()
        try:
            return session.query(Mission).filter(Mission.mission_id == mission_id).first()
        finally:
            session.close()

class CreateMission(graphene.Mutation):
    class Arguments:
        mission_date = graphene.Date(required=True)
        airborne_aircraft = graphene.Float()
        attacking_aircraft = graphene.Float()
        bombing_aircraft = graphene.Float()
        aircraft_returned = graphene.Float()
        aircraft_failed = graphene.Float()
        aircraft_damaged = graphene.Float()
        aircraft_lost = graphene.Float()

    mission = graphene.Field(lambda: MissionObject)

    def mutate(self, info, **kwargs):
        session = Session()
        try:
            mission = Mission(**kwargs)
            session.add(mission)
            session.commit()
            return CreateMission(mission=mission)
        finally:
            session.close()


schema = graphene.Schema(query=Query)