from django.utils import timezone
from polls .factories import ChoiceFactory
from polls .factories import QuestionFactory
from pytest_factoryboy import register
import datetime
import pytest

register(QuestionFactory, 'past_question', question_text="Past Question",
         pub_date=timezone.now() - datetime.timedelta(days=30))
register(QuestionFactory, 'future_question', question_text="Future Question",
         pub_date=timezone.now() + datetime.timedelta(days=30))
register(ChoiceFactory)


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    return chrome_options
