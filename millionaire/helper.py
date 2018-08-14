from millionaire.models import UserBestScore


def update_user_score(user, score):
    user_score, exists = UserBestScore.objects.get_or_create(user=user)
    if exists:
        if user_score.score > score:
            return
    user_score.score = score
    user_score.save()


def drop_session_data(request):
    request.session['given_questions'] = []
    request.session['user_total_scores'] = 0
    request.session['user_question_count'] = 0
