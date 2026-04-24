from fastapi import Header, Query


async def get_language(
    accept_language: str | None = Header(
        None,
        description="For persian please enter : fa " "For English please enter : en",
    ),
    lang: str | None = Query(
        None,
        description="For persian please enter : fa " "For English please enter : en",
    ),
):
    if lang:
        return lang

    if accept_language:
        return accept_language.split(",")[0]

    return "en"
