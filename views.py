from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # get selected choices
    selected_ids = request.POST.getlist('choices')
    selected_choices = Choice.objects.filter(id__in=selected_ids)

    # create submission
    submission = Submission.objects.create(
        user=request.user,
        course=course
    )
    submission.choices.set(selected_choices)
    submission.save()

    return redirect('show_exam_result', submission_id=submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    course = submission.course

    selected_choices = submission.choices.all()
    selected_ids = [choice.id for choice in selected_choices]

    total_score = 0
    possible_score = 0

    for question in course.lesson_set.first().question_set.all():
        possible_score += 1

        # correct choices for this question
        correct_choices = question.choice_set.filter(is_correct=True)

        # selected correct choices
        selected_correct = selected_choices.filter(
            question=question,
            is_correct=True
        )

        if set(correct_choices) == set(selected_correct):
            total_score += 1

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': total_score,
        'possible': possible_score
    }

    return render(request, 'exam_result_bootstrap.html', context)
