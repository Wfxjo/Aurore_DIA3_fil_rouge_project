import os

from google import genai
from google.genai import types

from calendar_tools import TOOL_FUNCTIONS, _to_json

IMAGE_MODEL = "gemini-nano-banana-2.1"
MAX_PROMPT_CHARS = 1000

_last_image = None


def pop_last_image():
    global _last_image
    image, _last_image = _last_image, None
    return image


def generate_image(prompt):
    global _last_image

    client = genai.Client(api_key=os.environ["GEMINI_KEY"])
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt[:MAX_PROMPT_CHARS],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        ),
    )

    for part in response.parts or []:
        if part.inline_data:
            _last_image = part.inline_data.data
            return _to_json({
                "statut": "image générée et affichée à l'utilisateur",
            })

    raise ValueError(
        "Aucune image renvoyée (demande peut-être refusée par le filtre "
        "de sécurité de Google)."
    )


TOOL_FUNCTIONS["generate_image"] = generate_image