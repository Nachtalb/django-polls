from django.utils import timezone
from polls.models import Choice
from polls.models import Question
import pytest


class TestQuestionFactory:
    @pytest.mark.django_db
    def test_question_factory_working(self, past_question, future_question,
                                      question_factory):
        """
        All `QuestionFactory` factories are working correctly.
        """
        question = question_factory.create()
        assert isinstance(past_question, Question)
        assert isinstance(future_question, Question)
        assert isinstance(question, Question)

    @pytest.mark.django_db
    def test_past_question_pub_date(self, past_question):
        """
        The `pub_date` of the registered `past_question` is in the past.
        """
        assert past_question.pub_date < timezone.now()

    @pytest.mark.django_db
    def test_future_question_pub_date(self, future_question):
        """
        The `pub_date` of the registered `future_question` is in the future.
        """
        assert future_question.pub_date > timezone.now()


class TestChoiceFactory:
    @pytest.mark.django_db
    def test_choice_factory_working(self, choice_factory):
        """
        The registered `ChoiceFactory` is working.
        """
        choice = choice_factory.create()
        assert isinstance(choice, Choice)

    @pytest.mark.django_db
    def test_choice_factory_has_question(self, choice_factory):
        """
        The `question` SubFactory of the `ChoiceFactory` is working.
        """
        choice = choice_factory.create()
        assert isinstance(choice.question, Question)
