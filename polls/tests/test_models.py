from django.utils import timezone
import pytest
import datetime


class TestQuestionModel:

    @pytest.mark.django_db
    def test_was_published_recently_with_future_question(self, future_question):
        """
        was_published_recently() returns false for questions whose pub_date is
        in the future
        """
        assert future_question.was_published_recently() is False

    @pytest.mark.django_db
    def test_was_published_recently_with_old_question(self, past_question):
        """
        was_published_recently() returns false for questions whose pub_date is
        older than 1 day
        """
        assert past_question.was_published_recently() is False

    @pytest.mark.django_db
    def test_was_published_recently_with_recent_question(self, past_question):
        """
        was_published_recently() returns true for questions whose pub_date is
        within the last day
        """
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        past_question.pub_date = time

        assert past_question.was_published_recently() is True
