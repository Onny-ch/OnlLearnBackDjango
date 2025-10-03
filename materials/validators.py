from rest_framework.serializers import ValidationError

permitted_words = ["youtube.com",]


def validate_permitted_words(value):
    counter = 0

    for address in permitted_words:
        if address not in value:
            counter += 1
    if counter > 0:
        raise ValidationError(
            f"Ссылка должна быть правильного формата на данные видеохостинги: {', '.join(permitted_words)}"
        )
