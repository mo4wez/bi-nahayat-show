pending_student_auth = set()


def set_waiting_for_student_id(chat_id: int):
    pending_student_auth.add(chat_id)


def clear_waiting_for_student_id(chat_id: int):
    pending_student_auth.discard(chat_id)


def is_waiting_for_student_id(chat_id: int) -> bool:
    return chat_id in pending_student_auth
