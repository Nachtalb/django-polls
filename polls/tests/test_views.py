from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
import pytest

from polls import factories


class QuestionIndexViewText(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    @freeze_time("Feb 1st, 2017")
    def test_past_questions(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        with freeze_time("Jan 1st, 2017"):
            factories.QuestionFactory(question_text='Past question.')
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    @freeze_time("Feb 1st, 2017")
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only the past questions
        are displayed.
        """
        with freeze_time("Jan 1st, 2017"):
            factories.QuestionFactory(question_text='Past question.')
        with freeze_time("Mar 1st, 2017"):
            factories.QuestionFactory(question_text='Past question.')
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    @freeze_time("Feb 1st, 2017")
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        with freeze_time("Jan 1st, 2017"):
            factories.QuestionFactory(question_text='Past question 1.')

        with freeze_time("Jan 2nd, 2017"):
            factories.QuestionFactory(question_text='Past question 2.')

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class TestQuestionDetailView:
    @freeze_time("Feb 1st, 2017")
    @pytest.mark.django_db
    def test_future_question(self, client):
        """
        The detail view of a question with a pub_date in the future returns a
        404 not found.
        """

        with freeze_time("Feb 5th, 2017"):
            future_question = factories.QuestionFactory(
                question_text='Future question.')

        url = reverse('polls:detail', args=(future_question.id,))
        response = client.get(url)

        assert response.status_code == 404

    @freeze_time("Feb 1st, 2017")
    @pytest.mark.django_db
    def test_past_question(self, client):
        """
        The detail view of a question with a pub_date in the past displays the
        question's text.
        """
        with freeze_time("Jan 28th, 2017"):
            past_question = factories.QuestionFactory(
                question_text='Past question.')

        url = reverse('polls:detail', args=(past_question.id,))
        response = client.get(url)

        assert past_question.question_text in str(response.content)


class TestQuestionVoteSelenium:
    def test_vote_fields_exist(self, selenium, live_server):
        """
        One submit button and two choice radio buttons are rendered.
        """
        question = factories.QuestionFactory(question_text='Test Question')
        factories.ChoiceFactory(choice_text="Choice 1", question=question)
        factories.ChoiceFactory(choice_text="Choice 2", question=question)

        selenium.get(
            live_server.url + reverse('polls:detail', args=(question.id,)))

        assert selenium.find_element_by_id('choice1')
        assert selenium.find_element_by_id('choice2')
        assert selenium.find_element_by_css_selector('input[type=submit]')

    def test_vote_can_submit_with_valid_data(self, live_server, selenium):
        """
        The application redirects from vote to results.
        """
        question = factories.QuestionFactory(question_text='Test Question')
        factories.ChoiceFactory(choice_text="Choice 1", question=question)
        factories.ChoiceFactory(choice_text="Choice 2", question=question)

        selenium.get(
            live_server.url + reverse('polls:detail', args=(question.id,)))
        selenium.find_element_by_id('choice1').click()
        selenium.find_element_by_css_selector('input[type=submit]').click()

        assert selenium.current_url == \
               live_server.url + reverse('polls:results', args=(question.id,))

    def test_vote_can_submit_with_invalid_data(self, live_server, selenium):
        """
        The application redirects back the the vote page if the sent data
        is invalid and an appropriate error message is shown.
        """
        question = factories.QuestionFactory(question_text='Test Question')
        factories.ChoiceFactory(choice_text="Choice 1", question=question)
        factories.ChoiceFactory(choice_text="Choice 2", question=question)

        selenium.get(
            live_server.url + reverse('polls:detail', args=(question.id,)))
        selenium.find_element_by_css_selector('input[type=submit]').click()

        assert selenium.current_url == \
               live_server.url + reverse('polls:vote', args=(question.id,))
        assert selenium.find_element_by_css_selector('body main p').text == \
            "You didn't select a choice."
