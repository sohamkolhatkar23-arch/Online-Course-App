from django.shortcuts import render, get_object_or_404
from .models import Course, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    selected_choices = request.POST.getlist('choices')
    selected_choices = Choice.objects.filter(id__in=selected_choices)

    submission = Submission.objects.create(
        user=request.user,
        course=course
    )
    submission.choices.set(selected_choices)

    total = selected_choices.count()
    correct = selected_choices.filter(is_correct=True).count()

    score = (correct / total) * 100 if total > 0 else 0
    submission.score = score
    submission.save()

    return show_exam_result(request, submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    context = {
        'submission': submission,
        'score': submission.score
    }

    return render(request, 'exam_result.html', context)
