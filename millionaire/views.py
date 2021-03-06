from collections import namedtuple

from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect

from millionaire.models import Choice, RandomQuestions, UserBestScore, Question

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from millionaire.helper import update_user_score, drop_session_data
from millionaire.game_settings import *
from configs.http_response_settings import NOT_ENOUGH_QUESTIONS


class Game(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get(self, request):
        top_scores = (UserBestScore.objects
                      .order_by('score')
                      .values_list('score', flat=True)
                      .distinct())
        print(top_scores)
        top_players = UserBestScore.objects.order_by('-score').filter(score__in=top_scores[:10])
        print(top_players)
        return render_to_response(self.template_name, {'top_players': top_players})

    def post(self, request):
        pass


class QuestionView(LoginRequiredMixin, TemplateView):
    template_name = "question.html"

    def get(self, request):
        ## In case we dont have enough questions the while loop will run forever

        game_total_question_count = Question.objects.count()
        print(game_total_question_count)
        if game_total_question_count < QUESTIONS_PER_GAME:
            return HttpResponse(NOT_ENOUGH_QUESTIONS)


        question = RandomQuestions.get_random()


        if len(request.session.get('given_questions',[] )) == game_total_question_count:
            request.session['given_questions'] = []
        given_questions = request.session.get('given_questions', [])
        while question.id in given_questions:
            question = RandomQuestions.get_random()
        given_questions.append(question.id)
        request.session['given_questions'] = given_questions


        ##refactor
        QuestionChoices = namedtuple("Choices",
                                     ['answer_text', 'is_answer', 'id'])
        question_choices = Choice.objects.values_list('answer_text', 'is_answer', 'id').filter(question=question).all()
        named_choices = [QuestionChoices(*c) for c in question_choices]

        return render_to_response(self.template_name, {'question': question, 'choices': named_choices})

    def post(self, request):

        ## count question count per game
        user_question_count = request.session.get('user_question_count', 0) + 1
        request.session['user_question_count'] = user_question_count

        question_id = request.POST['question']
        answer_ids = [int(request.POST[name]) for name in request.POST if name.startswith('answer')]
        right_answer_ids = list(
            Choice.objects.filter(question_id=question_id).filter(is_answer=True).values_list('id', flat = True))

        question_score = Question.objects.values_list("score", flat=True).get(id=question_id)


        if list(set(right_answer_ids) - set(answer_ids)) or list(set(answer_ids) - set(right_answer_ids)):
            user_total_scores = request.session.get('user_total_scores', 0)

            update_user_score(request.user, user_total_scores)
            drop_session_data(request)

            request.session['right_answer_ids'] = list(right_answer_ids)
            return redirect('finish', score=user_total_scores)

        else:
            user_total_scores = request.session.get('user_total_scores', 0) + question_score
            request.session['user_total_scores'] = user_total_scores

            if user_question_count >= QUESTIONS_PER_GAME:
                update_user_score(request.user, user_total_scores)
                drop_session_data(request)


                return redirect('finish', score = user_total_scores)
            else:
                return redirect('question')

class GameFinishView(LoginRequiredMixin, TemplateView):
    template_name = "game_over.html"
    def get(self, request, score):
        true_choice_ids = request.session.get('right_answer_ids', [])
        if true_choice_ids:
            del request.session['right_answer_ids']
        true_choices = Choice.objects.values_list('answer_text',flat = True).filter(id__in = true_choice_ids)
        return render_to_response(self.template_name, {'score': score,'true_choices': true_choices})
