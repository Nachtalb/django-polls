from django.utils import timezone
from faker import Factory as FakerFactory
import factory

faker = FakerFactory.create()


class QuestionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'polls.Question'

    question_text = factory.sequence(lambda n: faker.sentence(nb_words=4))
    pub_date = factory.sequence(lambda n: timezone.now())


class ChoiceFactory(factory.django.DjangoModelFactory):

    """Choice factory."""

    choice_text = factory.sequence(lambda n: faker.sentence(nb_words=4))

    class Meta:
        model = 'polls.Choice'

    question = factory.SubFactory(QuestionFactory)
