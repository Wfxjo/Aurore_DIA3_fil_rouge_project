import base64
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from CSSapp_UI import CUSTOM_CSS, PETALS_HTML, HEADER_HTML, CLOCK_WIDGET_HTML
from llm_agent import ConversationAgent

SESSION_KEY = "conversation_agent_object"

QUICK_ACTIONS = {
    "Mon agenda de la semaine":
        "Quels sont mes rendez-vous des 7 prochains jours ?",
    "Rédiger un mail": "Aide-moi à rédiger un mail.",
    "Créer une image": "Je voudrais générer une image.",
}


class UserInterface:
    def __init__(self):
        st.set_page_config(
            page_title="AURORE", initial_sidebar_state="expanded"
        )
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
        st.markdown(PETALS_HTML, unsafe_allow_html=True)
        st.markdown(HEADER_HTML, unsafe_allow_html=True)
        self.agent = self.get_persistent_agent()

    @staticmethod
    def get_persistent_agent():
        if SESSION_KEY not in st.session_state:
            st.session_state[SESSION_KEY] = ConversationAgent()

        return st.session_state[SESSION_KEY]

    @staticmethod
    def greeting():
        hour = datetime.now().hour
        if hour < 5 or hour >= 18:
            return "Bonsoir"
        if hour < 12:
            return "Bonjour"
        return "Bon après-midi"

    @staticmethod
    def show_label(text):
        st.markdown(
            f'<div class="hud-label">{text}</div>', unsafe_allow_html=True
        )

    @staticmethod
    def display_image(base64_image):
        image_bytes = base64.b64decode(base64_image.split(",", 1)[1])
        st.image(image_bytes, width=150)

    @staticmethod
    def display_message(message):
        with st.chat_message(message["role"]):
            for content in message["content"]:
                if content["type"] == "text":
                    st.markdown(content["text"])
                elif content["type"] == "image_url":
                    UserInterface.display_image(content["image_url"]["url"])

    def show_discussion_history(self, history):
        for message in history:
            self.display_message(message)

    def show_welcome(self):
        st.markdown(
            '<div class="hud-panel welcome">'
            '<div class="hud-label">Bienvenue</div>'
            f"<p>{self.greeting()}. Que puis-je faire pour vous aider "
            "à organiser vos évènements ?</p></div>",
            unsafe_allow_html=True,
        )

    def show_generated_image(self):
        generated_image = self.agent.get_last_image()
        if generated_image:
            st.image(generated_image, caption="Image générée")

    def render_sidebar(self):
        clicked_prompt = None

        with st.sidebar:
            self.show_label("Aujourd'hui")
            components.html(CLOCK_WIDGET_HTML, height=100)

            self.show_label("Accès rapide")
            for label, prompt in QUICK_ACTIONS.items():
                if st.button(label):
                    clicked_prompt = prompt

            self.show_label("Session")
            if st.button("Nouvelle conversation"):
                st.session_state.pop(SESSION_KEY, None)
                st.rerun()

        return clicked_prompt

    def read_user_input(self, quick_prompt, user_interaction):
        if quick_prompt:
            return quick_prompt, None
        if not user_interaction:
            return None, None

        if user_interaction.audio:
            text = self.agent.transcribe(user_interaction.audio.getvalue())
        else:
            text = user_interaction.text

        files = user_interaction.files
        image = files[0].getvalue() if files else None
        return text, image

    # def speak_last_response(self):
    #     text = self.agent.get_last_response_text()
    #     if not text:
    #         return
    #
    #     try:
    #         audio = self.agent.speak(text)
    #         st.audio(audio, format="audio/wav", autoplay=True)
    #     except Exception as error:
    #         st.warning(f"Synthèse vocale indisponible : {error}")

    def run(self):
        quick_prompt = self.render_sidebar()
        user_interaction = st.chat_input(
            "Que puis-je faire pour vous rendre service ?",
            accept_file=True,
            accept_audio=True,
            file_type=["jpg", "jpeg", "png"],
        )

        with st.spinner("AURORE réfléchit…"):
            text, image = self.read_user_input(quick_prompt, user_interaction)
            if text or image:
                self.agent.ask_llm(text, image)

        history = self.agent.get_conversation_history()
        if history:
            self.show_discussion_history(history)
        else:
            self.show_welcome()

        self.show_generated_image()
        # self.speak_last_response()


if __name__ == "__main__":
    user_interface_object = UserInterface()
    user_interface_object.run()