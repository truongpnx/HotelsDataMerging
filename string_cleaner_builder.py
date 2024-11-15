import re
import html
import unicodedata


class StringCleanerBuilder:
    def __init__(self) -> None:
        self.steps = []

    def strip_whitespace(self):
        self.steps.append(lambda data: data.strip())
        return self

    def to_lowercase(self):
        self.steps.append(lambda data: data.lower())
        return self

    def to_titlecase(self):
        self.steps.append(lambda data: data.title())
        return self

    def to_camelcase(self):
        def camel_case_conversion(data):
            words = re.split(r'\s+|(?<=[a-z])(?=[A-Z])', data)
            words = [word.capitalize() for word in words if word]
            
            return words[0].lower() + ''.join(words[1:]) if words else ""

        self.steps.append(camel_case_conversion)
        return self

    def remove_camelcase(self):
        self.steps.append(lambda data: re.sub(r"(?<=[a-z])([A-Z])", r" \1", data))
        return self

    def remove_special_characters(self, allowed_chars=""):
        self.steps.append(
            lambda data: re.sub(rf"[^a-zA-Z0-9{re.escape(allowed_chars)}]", "", data)
        )
        return self

    def escape_html(self):
        self.steps.append(lambda data: html.escape(data))
        return self

    def truncate(self, max_length):
        self.steps.append(lambda data: data[:max_length])
        return self

    def normalize_unicode(self):
        self.steps.append(lambda data: unicodedata.normalize("NFKC", data))
        return self

    def build(self):
        def cleaner(data):
            for step in self.steps:
                data = step(data)
            return data

        return cleaner


if __name__ == "__main__":
    cleaner = (
        StringCleanerBuilder()
        .strip_whitespace()
        .remove_camelcase()
        .remove_special_characters(allowed_chars="-_ ")
        .escape_html()
        .build()
    )

    data = "  Hello, World! Welcome to theBuilderPattern! 😀 "
    cleaned_data = cleaner(data)
    print(cleaned_data)
