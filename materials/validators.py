from rest_framework.serializers import ValidationError

permitted_words = [
    "youtube.com",
]


class ValidatePermittedWords:
    def __init__(self, field):
        self.field = field

    def __call__(self, url):
        counter = 0

        for address in permitted_words:
            if address not in url["video_url"]:
                counter += 1

        if counter > 0:
            raise ValidationError(
                f"Ссылка должна быть правильного формата на данные видеохостинги: {', '.join(permitted_words)}"
            )
