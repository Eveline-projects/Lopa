import uuid
import pytest
from apps.submissions.models import Submission
from apps.submissions.repositories import SubmissionRepository
from apps.problems.models import Problem


@pytest.mark.django_db
class TestSubmissionRepository:
    def test_create_should_return_saved_submission(self, user, problem):
        submission = SubmissionRepository.create(
            user=user,
            problem=problem,
            code='[4,5,6]',
        )

        assert submission.id is not None
        assert submission.user == user
        assert submission.problem == problem
        assert submission.code == '[4,5,6]'
        assert submission.status == Submission.Status.PENDING

    def test_gest_submissions_for_problem_should_return_all_submissions(
        self, user, problem
    ):
        Submission.objects.create(user=user, problem=problem, code='[1,2,3]')
        Submission.objects.create(user=user, problem=problem, code='[4,5,6]')

        queryset = SubmissionRepository.get_submissions_for_problem(problem.id)
        assert queryset.count() == 2
        code = {tc.code for tc in queryset}
        assert code == {'[1,2,3]', '[4,5,6]'}

    def test_get_by_id_should_return_submission(self, user, problem):
        created = Submission.objects.create(
            user=user,
            problem=problem,
            code='[4,5,6]',
        )

        submission = SubmissionRepository.get_by_id(created.id)
        assert submission == created
        assert submission.status == Submission.Status.PENDING

    def test_get_submissions_for_problem_should_not_include_other_problem_submissions(
        self, user, problem
    ):
        other_problem = Problem.objects.create()

        first = Submission.objects.create(
            user=user,
            problem=problem,
            code='[1,2,3]',
        )
        second = Submission.objects.create(
            user=user,
            problem=problem,
            code='[4,5,6]',
        )
        other_submission = Submission.objects.create(
            user=user,
            problem=other_problem,
            code='[7,8,9]',
        )

        submissions = list(
            SubmissionRepository.get_submissions_for_problem(problem.id)
        )

        assert len(submissions) == 2
        assert first in submissions
        assert second in submissions
        assert other_submission not in submissions

    def test_get_submissions_for_problem_should_return_submissions_by_created_at(
        self, user, problem
    ):
        first = Submission.objects.create(
            user=user,
            problem=problem,
            code='[1,2,3]',
        )
        second = Submission.objects.create(
            user=user,
            problem=problem,
            code='[4,5,6]',
        )

        submissions = list(
            SubmissionRepository.get_submissions_for_problem(problem.id)
        )

        assert submissions[0].id == second.id
        assert submissions[1].id == first.id

    def test_get_submissions_for_problem_should_return_submissions_ordered_by_created_at_desc(
        self, user, problem
    ):
        first = Submission.objects.create(
            user=user,
            problem=problem,
            code='[1,2,3]',
        )
        second = Submission.objects.create(
            user=user,
            problem=problem,
            code='[4,5,6]',
        )

        submissions = list(
            SubmissionRepository.get_submissions_for_problem(problem.id)
        )
        assert len(submissions) == 2
        assert submissions[0] == second
        assert submissions[1] == first

    def test_get_by_id_raises_does_not_exist(self):
        submission = SubmissionRepository.get_by_id(uuid.uuid4())

        assert submission is None
