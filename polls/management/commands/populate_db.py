from django.core.management.base import BaseCommand
from faker import Faker
from polls.models import User, Module, Resource
import random

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 10
    RESOURCE_COUNT = 1

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        # self.seed_modules()
        self.seed_resources()
        # self.seed_users()

    def seed_users(self):
        user_count = 0
        while user_count < Command.USER_COUNT:
            self._create_user()
            user_count += 1
            # print(f'Seeding user {user_count}',  end='\r')
            # try:
            #     self._create_user()
            # except (django.db.utils.IntegrityError):
            #     continue
            # user_count += 1
        print(f'---{user_count} Users seeded successfully----')
        
    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self._email(first_name, last_name)
        username = self._username(len(User.objects.all()))
        modules = Module.objects.order_by('?')[:3]
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Command.PASSWORD,
        )
        for m in modules:
            user.modules.add(m)

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email

    def _username(self, id):
        username = f'ID000{id}'
        return username

    def seed_modules(self):
        modules = [("4CCSIC", "Intro to Computing"), ("4CCSIA", "Intro to AI"), ("4CCSIC", "Intro to Computing"), ("4CCSIML", "Intro to Machine Learning")]
        for m in modules:
            module = Module.objects.create(module_code=m[0], module_name=m[1])
            module.save()
            
        print(f'---{len(modules)} Modules seeded successfully----')
    
    def create_resource(self):
        types = ["VIDEO", "DOCUMENT", "READING", "ARTICLE", "OTHER"]
        importances = ["MANDATORY", "OPTIONAL", "RECOMMENDED"]
        weeks = ["WEEK 1", "WEEK 2","WEEK 3", "WEEK 4","WEEK 5"]

        # n = random(0,(Module.objects.all.count-1))
        module = random.choice(Module.objects.all())
        resource_name = self.faker.sentence(nb_words=3)
        resource_type = random.choice(types)
        recommended_time_in_minutes = random.randint(5,90)
        importance = random.choice(importances)
        scheduled_week = random.choice(weeks)
        
        resource = Resource.objects.create(
            module = module,
            resource_name = resource_name,
            resource_type = resource_type,
            recommended_time_in_minutes = recommended_time_in_minutes,
            importance =importance,
            scheduled_week = scheduled_week
        )
        resource.save()
        
    def seed_resources(self):
        resource_count = 0
        while resource_count < self.RESOURCE_COUNT:
            self.create_resource()
            resource_count+=1
            
        print(f'---{resource_count} Resources seeded successfully----')
