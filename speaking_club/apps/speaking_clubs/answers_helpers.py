
from uuid import UUID
from speaking_clubs import models


def _get_current_student(user: models.User) -> models.Student:
    user = models.Student.objects.get(user=user)
    return user


def register_answer(user: models.User, quiz_id: UUID, answer: dict):
    user = _get_current_student(user=user)

    answer, _ = models.Answer.objects.get_or_create(
        quiz_id=quiz_id,
        answer=answer,
    )

    answer.users.add(user)

    return True


def get_answers(user: models.User, quiz_ids: list[UUID]) -> list[dict]:
    user = _get_current_student(user=user)

    answers = models.Answer.objects.filter(
        users__id__exact=user.id,
        quiz_id__in=quiz_ids,
    ).all()

    return [{"quiz_id": answer.quiz_id, "answer": answer.answer} for answer in answers]
