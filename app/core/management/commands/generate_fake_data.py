from django.core.management.base import BaseCommand
from faker import Faker
from core.models import User, Recipe, Tag
from decimal import Decimal

faker = Faker()

class Command(BaseCommand):  # The class name must be `Command`
    help = 'Generate fake data for testing'

    def handle(self, *args, **kwargs):
        self.create_fake_data()

    def create_fake_data(self):
        users = self.create_users(10)
        tags = self.create_tags(users, 20)
        self.create_recipes(users, tags, 50)
        self.stdout.write(self.style.SUCCESS('Fake data created successfully!'))

    def create_users(self, n=5):
        users = []
        for _ in range(n):
            name = f"User_{_}"
            email = f"{name}@user.com"
            password = "test123456"
            user = User.objects.create_user(email=email, name=name, password=password)
            users.append(user)
        return users

    def create_tags(self, users, n=10):
        tags = []
        for _ in range(n):
            name = faker.word()
            user = faker.random_element(users)
            tag = Tag.objects.create(name=name, user=user)
            tags.append(tag)
        return tags

    def create_recipes(self, users, tags, n=20):
        for _ in range(n):
            title = faker.sentence(nb_words=4)
            description = faker.text()
            time_minutes = faker.random_int(min=1, max=120)
            price = Decimal(faker.random_int(min=100, max=5000) / 100)
            link = faker.url()
            user = faker.random_element(users)
            recipe = Recipe.objects.create(
                title=title,
                description=description,
                time_minutes=time_minutes,
                price=price,
                link=link,
                user=user
            )
            recipe.tags.add(*faker.random_elements(tags, length=faker.random_int(min=1, max=3)))
