import pytest
from unittest.mock import Mock
from backend.services import ProgramService


@pytest.fixture
def mock_repos():
    student_repo = Mock()
    exam_result_repo = Mock()
    assignment_repo = Mock()
    return student_repo, exam_result_repo, assignment_repo


def test_generate_study_program_no_student(mock_repos):
    student_repo, exam_result_repo, assignment_repo = mock_repos
    student_repo.get.return_value = None
    service = ProgramService(student_repo, exam_result_repo, assignment_repo)

    result = service.generate_study_program(1)
    assert result == "Öğrenci bulunamadı, lütfen ID’yi kontrol et."