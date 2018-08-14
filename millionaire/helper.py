from millionaire.models import UserBestScore


def update_user_score(user, score):
    exist_user_score = UserBestScore.objects.filter(user=user)
    if not exist_user_score:
        user_score = UserBestScore(user = user, score = score)
        user_score.save()
    else:
        user_score = UserBestScore.objects.get(user=user)
        if user_score.score < score:
            user_score.score = score
            user_score.save()


def drop_session_data(request):
    # del request.session['given_questions']
    # del request.session['user_total_scores']
    # del request.session['user_question_count']
    request.session['given_questions'] = []
    request.session['user_total_scores'] = 0
    request.session['user_question_count'] = 0
