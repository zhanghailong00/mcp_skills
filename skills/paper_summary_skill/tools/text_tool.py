def clean_text(text: str):

    text = text.strip()

    text = text.replace("\n\n", "\n")

    return text
