from django.urls import reverse
from django.utils import timezone
from polls.models import Question
import datetime
import pytest


class TestQuestionIndexView:
    @pytest.mark.django_db
    def test_no_questions(self, client):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = client.get(reverse('polls:index'))

        assert response.status_code == 200
        assert 'No polls are available' in str(response.content)
        assert set(tuple(response.context['latest_question_list'])) == \
               set(Question.objects
                   .filter(pub_date__lte=timezone.now())
                   .order_by('-pub_date')[:5])

    @pytest.mark.django_db
    def test_past_questions(self, client, past_question):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        response = client.get(reverse('polls:index'))

        assert set(tuple(response.context['latest_question_list'])) == \
            set(Question.objects
                .filter(pub_date__lte=timezone.now())
                .order_by('-pub_date')[:5])

    @pytest.mark.django_db
    def test_future_question_and_past_question(self, client, past_question,
                                               future_question):
        """
        Even if both past and future questions exist, only the past questions
        are displayed.
        """
        response = client.get(reverse('polls:index'))

        assert set(tuple(response.context['latest_question_list'])) == \
               set(Question.objects
                   .filter(pub_date__lte=timezone.now())
                   .order_by('-pub_date')[:5])

    @pytest.mark.django_db
    def test_two_past_questions(self, client, past_question, question_factory):
        """
        The questions index page may display multiple questions.
        """
        # create a second one in the past.
        question_factory(question_text='Past question.',
                         pub_date=timezone.now() - datetime.timedelta(days=20))
        response = client.get(reverse('polls:index'))

        assert set(tuple(response.context['latest_question_list'])) == \
               set(Question.objects
                   .filter(pub_date__lte=timezone.now())
                   .order_by('-pub_date')[:5])


class TestQuestionDetailView:
    @pytest.mark.django_db
    def test_future_question(self, client, future_question):
        """
        The detail view of a question with a pub_date in the future returns a
        404 not found.
        """
        url = reverse('polls:detail', args=(future_question.id,))
        response = client.get(url)

        assert response.status_code == 404

    @pytest.mark.django_db
    def test_past_question(self, client, past_question):
        """
        The detail view of a question with a pub_date in the past displays the
        question's text.
        """
        url = reverse('polls:detail', args=(past_question.id,))
        response = client.get(url)

        assert past_question.question_text in str(response.content)


class TestQuestionVoteSelenium:
    def test_vote_fields_exist(self, selenium, live_server, past_question,
                               choice_factory):
        """
        One submit button and two choice radio buttons are rendered.
        """
        choice_factory(choice_text="Choice 1", question=past_question)
        choice_factory(choice_text="Choice 2", question=past_question)

        selenium.get(live_server.url + reverse('polls:detail',
                                               args=(past_question.id,)))

        assert selenium.find_element_by_id('choice1')
        assert selenium.find_element_by_id('choice2')
        assert selenium.find_element_by_css_selector('input[type=submit]')

    def test_vote_can_submit_with_valid_data(self, live_server, selenium,
                                             past_question, choice_factory):
        """
        The application redirects from vote to results.
        """
        choice_factory(choice_text="Choice 1", question=past_question)
        choice_factory(choice_text="Choice 2", question=past_question)

        selenium.get(live_server.url + reverse('polls:detail',
                                               args=(past_question.id,)))
        selenium.find_element_by_id('choice1').click()
        selenium.find_element_by_css_selector('input[type=submit]').click()

        assert selenium.current_url == \
               live_server.url + reverse('polls:results', args=(past_question.id,))

    def test_vote_can_submit_with_invalid_data(self, live_server, selenium,
                                               past_question, choice_factory):
        """
        The application redirects back the the vote page if the sent data
        is invalid and an appropriate error message is shown.
        """
        choice_factory(choice_text="Choice 1", question=past_question)
        choice_factory(choice_text="Choice 2", question=past_question)

        selenium.get(live_server.url + reverse('polls:detail',
                                               args=(past_question.id,)))
        selenium.find_element_by_css_selector('input[type=submit]').click()

        assert selenium.current_url == \
               live_server.url + reverse('polls:vote', args=(past_question.id,))
        assert selenium.find_element_by_css_selector('body main p').text == \
            "You didn't select a choice."
