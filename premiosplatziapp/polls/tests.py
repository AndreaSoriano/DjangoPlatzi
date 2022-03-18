import datetime
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone
from .models import Question

# Se pueden testear Models o Views

class QuestionModelTests(TestCase):

    def setUp(self):
        self.question = Question(
            question_text="¿Quién es el mejor Course Director de Platzi?")

    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False for question whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)
        # self.assertEqual(future_question.was_published_recently(),False)
    
    def test_was_published_recently_with_present_question(self):
        """was_published_recently returns True for question whose pub_date is in the present"""
        time = timezone.now() - datetime.timedelta(hours=13)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)
        # self.assertEqual(future_question.was_published_recently(),False)
    
    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns False for question whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)
        # self.assertEqual(future_question.was_published_recently(),False)

def create_question(question_text, days):
    """Create a question with the given "question_text", and published the given number of days 
    offset to now (negative for questions published in the past, positive for questions that 
    have yet to be published)"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question(self):
        """Questions qwith a pub_date in the future aren't displayed on the index page"""
        create_question("Future question",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question(self):
        """Questions with a pub_date in the past are displayed on the index page"""
        question = create_question("Past question",days=-20)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

