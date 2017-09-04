import datetime

from django.utils import timezone

from polls import factories


class TestQuestionModel:
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns false for questions whose pub_date is
        in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = factories.QuestionFactory.build(pub_date=time)

        assert future_question.was_published_recently() is False

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns false for questions whose pub_date is
        older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_question = factories.QuestionFactory.build(pub_date=time)

        assert future_question.was_published_recently() is False

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns true for questions whose pub_date is
        within the last day
        """
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        future_question = factories.QuestionFactory.build(pub_date=time)

        assert future_question.was_published_recently() is True
