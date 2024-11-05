import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy.sql import func
from .models import Country, City, TargetType, Target, Mission
from .database import Session
from graphql import GraphQLError


# Service Classes
class IdGeneratorService:
    @staticmethod
    def get_next_mission_id():
        last_id = Session.query(func.max(Mission.mission_id)).scalar() or 0
        return last_id + 1


# GraphQL Object Types
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


# Query Class
class Query(graphene.ObjectType):
    # Query Fields
    all_missions = graphene.List(MissionObject)
    mission_by_id = graphene.Field(MissionObject, mission_id=graphene.Int(required=True))
    missions_by_date_range = graphene.List(
        MissionObject,
        start_date=graphene.Date(required=True),
        end_date=graphene.Date(required=True)
    )
    missions_by_country = graphene.List(MissionObject, country_name=graphene.String(required=True))
    missions_by_target_industry = graphene.List(MissionObject, industry=graphene.String(required=True))
    attack_results_by_target_type = graphene.List(MissionObject, target_type=graphene.String(required=True))

    # Resolvers
    def resolve_all_missions(self, info):
        return Session.query(Mission).all()

    def resolve_mission_by_id(self, info, mission_id):
        mission = Session.query(Mission).filter(Mission.mission_id == mission_id).first()
        if not mission:
            raise GraphQLError(f"Mission with id {mission_id} not found")
        return mission

    def resolve_missions_by_date_range(self, info, start_date, end_date):
        return Session.query(Mission).filter(
            Mission.mission_date.between(start_date, end_date)
        ).all()

    def resolve_missions_by_country(self, info, country_name):
        return Session.query(Mission).join(Target).join(City).join(Country).filter(
            Country.country_name == country_name
        ).all()

    def resolve_missions_by_target_industry(self, info, industry):
        return Session.query(Mission).join(Target).filter(
            Target.target_industry == industry
        ).all()


    def resolve_attack_results_by_target_type(self, info, target_type):
        mission_result_attack =Session.query(Mission).join(Target).join(TargetType).filter(TargetType.target_type_name == target_type).all()
        if not mission_result_attack:
            raise GraphQLError(f"Mission with target {target_type} not found")
        return mission_result_attack


# Mutation Classes
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
        kwargs['mission_id'] = IdGeneratorService.get_next_mission_id()

        mission = Mission(**kwargs)
        Session.add(mission)
        Session.commit()
        return CreateMission(mission=mission)


class AddTarget(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        target_industry = graphene.String(required=True)
        city_id = graphene.Int(required=True)
        target_type_id = graphene.Int(required=True)
        target_priority = graphene.Int()

    target = graphene.Field(lambda: TargetObject)

    def mutate(self, info, **kwargs):
        target = Target(**kwargs)
        Session.add(target)
        Session.commit()
        return AddTarget(target=target)


class UpdateAttackResults(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        aircraft_returned = graphene.Float()
        aircraft_failed = graphene.Float()
        aircraft_damaged = graphene.Float()
        aircraft_lost = graphene.Float()

    mission = graphene.Field(lambda: MissionObject)

    def mutate(self, info, mission_id, **kwargs):
        mission = Session.query(Mission).filter(Mission.mission_id == mission_id).first()
        if not mission:
            raise GraphQLError(f"Mission with id {mission_id} not found")

        for key, value in kwargs.items():
            setattr(mission, key, value)
        Session.commit()
        return UpdateAttackResults(mission=mission)


class DeleteMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, mission_id):
        mission = Session.query(Mission).filter(Mission.mission_id == mission_id).first()
        if not mission:
            raise GraphQLError(f"Mission with id {mission_id} not found")

        Session.delete(mission)
        Session.commit()
        return DeleteMission(success=True)


# Root Mutation Type
class Mutation(graphene.ObjectType):
    create_mission = CreateMission.Field()
    add_target = AddTarget.Field()
    update_attack_results = UpdateAttackResults.Field()
    delete_mission = DeleteMission.Field()


# Schema Definition
schema = graphene.Schema(query=Query, mutation=Mutation)