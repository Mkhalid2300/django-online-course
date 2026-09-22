from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course, Enrollment, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse/course_list.html', {'courses': courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


@login_required
def exam(request, course_id):
    """Displays the exam form with all questions and choices for a course."""
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.all()
    return render(request, 'onlinecourse/exam_bootstrap.html', {'course': course, 'questions': questions})


@login_required
def submit(request, course_id):
    """
    Handles submission of the exam for a given course.
    Creates a Submission object linked to the learner's Enrollment,
    and records the choices they selected.
    """
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = request.POST.getlist('choice')
    submission.choices.set(selected_choices)

    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course.id, submission.id))
    )


def show_exam_result(request, course_id, submission_id):
    """
    Evaluates a submission and displays the learner's score,
    including which questions were answered correctly.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()
    selected_choice_ids = [choice.id for choice in selected_choices]

    total_score = 0
    questions = course.questions.all()
    for question in questions:
        if question.is_get_score(selected_choice_ids):
            total_score += question.question_grade

    context = {
        'course': course,
        'submission': submission,
        'selected_choices': selected_choices,
        'total_score': total_score,
        'questions': questions,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)