from groq import Groq
import base64
import json
from dotenv import load_dotenv
import os
from datetime import datetime

from calendar_tools import run_tool
from image_tools import pop_last_image
from quote_tools import pop_last_quote
from tool_schemas import CALENDAR_TOOLS

MAX_TOOL_ROUNDS = 5


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.conversation_history = [
                {
                    "role": "system",
                    "content": self.read_file(file_path="./context.txt")
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    @staticmethod
    def encode_image(image):
        return base64.b64encode(image).decode('utf-8')


    def get_conversation_history(self):
        return self.conversation_history[1: ]


    def get_last_response_text(self):
        content = self.conversation_history[-1]["content"]
        return content[0]["text"] if content else ""


    @staticmethod
    def get_last_image():
        return pop_last_image()


    @staticmethod
    def get_last_quote():
        return pop_last_quote()


    @staticmethod
    def build_content(text_interaction, image=None):
        content = []
        if text_interaction:
            content.append({
                            "type": "text",
                            "text": text_interaction
                        })
        if image :
            content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{ConversationAgent.encode_image(image)}",
                            },
                        })

        return content


    def update_conversation_history(self, role, text_interaction, image=None):
        self.conversation_history.append(
            {
            "role": role,
            "content": self.build_content(text_interaction, image),
            }
        )



    def transcribe(self, audio_interaction):

        transcription = self.groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_interaction),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            timestamp_granularities = ["word", "segment"],
            temperature=0.0
        )

        return transcription.text



    def ask_llm(self, text_interaction, image):

        self.update_conversation_history(role="user", text_interaction=text_interaction, image=image)

        # Copie locale : les messages d'outils ne doivent pas apparaître dans l'historique affiché
        messages = list(self.conversation_history)
        messages.insert(1, {
            "role": "system",
            "content": f"Date et heure actuelles : {datetime.now():%A %d %B %Y, %H:%M}.",
        })

        response = "Je n'ai pas réussi à terminer : trop d'appels d'outils successifs."

        for _ in range(MAX_TOOL_ROUNDS):
            message = self.groq_client.chat.completions.create(
                messages=messages,
                model="qwen/qwen3.8-27b",
                include_reasoning=False,
                tools=CALENDAR_TOOLS,
                temperature=0,
            ).choices[0].message

            if not message.tool_calls:
                response = message.content
                break

            messages.append(message)
            for tool_call in message.tool_calls:
                arguments = json.loads(tool_call.function.arguments or "{}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": run_tool(tool_call.function.name, arguments),
                })

        self.update_conversation_history(role="assistant", text_interaction=response)


if __name__ == "__main__":
    agent = ConversationAgent()
    agent.ask_llm(input("Pose ta question :\n"), None)
    print("\n", agent.get_last_response_text())