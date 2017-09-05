from django.utils import timezone
from faker import Factory as FakerFactory
from polls.models import Choice
from polls.models import Question
import factory

faker = FakerFactory.create()


class QuestionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Question

    question_text = factory.sequence(lambda n: faker.sentence(nb_words=4))
    pub_date = factory.sequence(lambda n: timezone.now())


class ChoiceFactory(factory.django.DjangoModelFactory):

    choice_text = factory.sequence(lambda n: faker.sentence(nb_words=4))

    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
