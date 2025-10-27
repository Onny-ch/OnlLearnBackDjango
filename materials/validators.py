from rest_framework.serializers import ValidationError

permitted_words = [
    "youtube.com",
]


class ValidatePermittedWords:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        print("DEBUG: value =", value)  # Что приходит?
        print("DEBUG: type =", type(value))  # Это строка?
        if not value:
            return
        if not any(address in value for address in permitted_words):
            raise ValidationError(
                f"Ссылка должна быть правильного формата на данные видеохостинги: {', '.join(permitted_words)}"
            )
