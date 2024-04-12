from django.core.management.base import BaseCommand
from faker import Faker
from polls.models import User, Module, Resource, Plan, Reflection
import datetime
from django.utils import timezone
import random

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 10
    RESOURCE_COUNT = 150

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.seed_modules()
        self.seed_resources()
        self.seed_users()
        self.seed_test_data()

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
        
    def _create_inactive_user(self, name, surname, username):
        first_name = name
        last_name = surname
        email = self._email(first_name, last_name)
        username = f'{first_name}.{last_name}'
        modules = Module.objects.order_by('?')[:4]
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_unusable_password()
        for m in modules:
            user.modules.add(m)
            
    def _create_active_user(self, name, surname, username):
        first_name = name
        last_name = surname
        email = self._email(first_name, last_name)
        username = f'{first_name}.{last_name}'
        modules = Module.objects.order_by('?')[:4]
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Command.PASSWORD,
        )
        for m in modules:
            user.modules.add(m)
            
    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self._email(first_name, last_name)
        username = self._username(len(User.objects.all()))
        modules = Module.objects.order_by('?')[:4]
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
        modules = [("6CCSIC", "Intro to Computing"), ("6CCSIA", "Intro to AI"), ("6CCSIR", "Intro to Robotics"), ("6CCSIML", "Intro to Machine Learning")]
        for m in modules:
            module = Module.objects.create(module_code=m[0], module_name=m[1])
            module.save()
            
        print(f'---{len(modules)} Modules seeded successfully----')
    
    def create_resource(self):
        types = ["VIDEO", "DOCUMENT", "READING", "ARTICLE", "OTHER"]
        importances = ["MANDATORY", "OPTIONAL", "RECOMMENDED"]
        weeks = ["WEEK 1", "WEEK 2","WEEK 3", "WEEK 4","WEEK 5"]

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
        
    def seed_test_data(self):
        weeks = ["WEEK 1", "WEEK 2","WEEK 3"]
        
        plan_1 = Plan.objects.create(
            week_plan = weeks[0],
            time_plan =  f'Begin with a 5-minute warm-up each day, followed by 25-minute  study sessions with 5-minute breaks. Repeat this cycle for 2 hours daily, then take longer breaks',
            study_method = f'This week, Im planning to try out the Pomodoro Technique. It seems like a great way to structure my study sessions with 25 minutes of focused work followed by 5-minute breaks. I hope it helps me stay productive while avoiding burnout.',
            created_at = (timezone.now() - datetime.timedelta(days=21))
        )
        plan_1.save()
        
        plan_2 = Plan.objects.create(
            week_plan = weeks[1],
            time_plan = f'Days 1-5: Kick off with a 10-minute warm-up, then study for 30 minutes with 5-minute breaks. Keep it going for 3 hours a day, and make sure to take some nice, long breaks in between.',
            study_method = "I've decided to incorporate spaced repetition into my study routine this week. Using flashcards and online tools, I'll review material at increasing intervals. It sounds like a smart strategy for reinforcing learning and improving retention.",
            created_at = (timezone.now() - datetime.timedelta(days=14)),
        )
        plan_2.save()
        
        plan_3 = Plan.objects.create(
            week_plan = weeks[2],
            time_plan = f'Warm-up: 10 mins Study Session: 30 mins Break: 5 mins Repeat: 3 times Total Time: 2 hours',
            study_method = "For my study plan this week, I'm going to experiment with time-blocking. By dividing my day into manageable chunks and assigning specific tasks to each block, I hope to boost my productivity and stay more organized. It feels empowering to take control of my schedule like this.",
            created_at = (timezone.now() - datetime.timedelta(days=8))
        )
        plan_3.save()
        
        print(f'--- Plans seeded successfully----')
        
        reflection_1 = Reflection.objects.create(
            plan_reflection = plan_1,
            time_reflection = "Trying the Pomodoro Technique helped me stay focused, but I found 25 minutes too short for deep work. Extending to 40-minute sessions felt more productive.",
            study_method_reflection = "Spaced repetition worked wonders for remembering facts, but it felt tedious. Adding variety, like mind maps, made review sessions more engaging",
            carry_forward_reflection = "Adapting techniques keeps learning interesting",
            created_at = (plan_1.created_at + datetime.timedelta(days=7)),
        )
        reflection_1.save()
        
        reflection_2 = Reflection.objects.create(
            plan_reflection = plan_2,
            time_reflection = "Time-blocking initially felt rigid, but breaking tasks into smaller chunks helped manage overwhelming workload. I also enjoyed the sense of accomplishment after completing each block",
            study_method_reflection = "Extending Pomodoro sessions allowed for deeper focus, but longer breaks felt disruptive. Shortening to 3-minute breaks maintained momentum without sacrificing rest.",
            carry_forward_reflection = "Breaking tasks into smaller pieces makes them more manageable",
            created_at = (plan_1.created_at + datetime.timedelta(days=7)),
        )
        reflection_2.save()
        
        print(f'--- Reflections seeded successfully----')
        
        # seed test inactive users 
        in_active_user = self._create_inactive_user(self, "Jack", "Doe")
        print(f'--- Test in_active User successfully----')
        
        # seed test active users 
        active_user = self._create_active_user(self, "Peter", "Piper")
        active_user.add_plan(plan_1)
        active_user.add_plan(plan_1)
        active_user.save()
        print(f'--- Test active User successfully----')
        
        
        
        
        
        
        
