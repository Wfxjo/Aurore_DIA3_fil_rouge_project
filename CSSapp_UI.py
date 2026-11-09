CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400&family=DM+Mono:wght@300;400&family=Jost:wght@300;400&display=swap');

    :root {
        --cream: #FBF4EE;
        --blush: #F6E0D6;
        --peach: #F2C9BB;
        --rose: #D98B84;
        --rose-gold: #C99A86;
        --charcoal: #3B3533;
        --ash: #6E6561;
    }

    /* ---------- Fond : aurore douce qui dérive lentement ---------- */
    .stApp {
        background:
            radial-gradient(40rem 30rem at 12% 8%, rgba(242, 201, 187, 0.75), transparent 65%),
            radial-gradient(36rem 30rem at 92% 18%, rgba(217, 139, 132, 0.28), transparent 65%),
            radial-gradient(44rem 34rem at 50% 105%, rgba(226, 210, 201, 0.9), transparent 65%),
            var(--cream);
        background-size: 140% 140%, 140% 140%, 140% 140%, auto;
        animation: aurora-drift 45s ease-in-out infinite alternate;
        font-family: 'Jost', sans-serif;
        font-weight: 300;
        color: var(--charcoal);
    }
    @keyframes aurora-drift {
        from { background-position: 0% 0%, 100% 0%, 50% 100%, 0 0; }
        to   { background-position: 100% 100%, 0% 100%, 50% 0%, 0 0; }
    }
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }
    .block-container { padding-top: 1rem; max-width: 820px; }
    ::selection { background: var(--peach); }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: var(--rose-gold); border-radius: 3px; }

    /* ---------- Couleurs de texte : tous les fonds sont clairs, texte foncé ---------- */
    .stApp,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stSidebar"] label,
    [data-testid="stSpinner"] * {
        color: var(--charcoal) !important;
    }
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: var(--ash) !important;
    }
    [data-testid="stChatMessage"] code,
    [data-testid="stChatMessage"] pre {
        background: rgba(242, 201, 187, 0.45) !important;
        color: var(--charcoal) !important;
    }

    /* ---------- Pétales qui tombent ---------- */
    .petals {
        position: fixed;
        inset: 0;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }
    .petal {
        position: absolute;
        top: -6%;
        width: var(--s, 12px);
        height: calc(var(--s, 12px) * 1.3);
        background: linear-gradient(135deg, #F7D5CB, #E39A91);
        border-radius: 150% 0 150% 0;
        opacity: 0;
        animation: petal-fall linear infinite;
    }
    @keyframes petal-fall {
        0%   { transform: translate3d(0, -5vh, 0) rotate(0deg); opacity: 0; }
        10%  { opacity: 0.45; }
        90%  { opacity: 0.35; }
        100% { transform: translate3d(var(--dx, 6vw), 105vh, 0) rotate(540deg); opacity: 0; }
    }

    /* ---------- En-tête : orbe HUD ---------- */
    .hud-header { text-align: center; }
    .hud-orb {
        position: relative;
        width: 190px;
        height: 190px;
        margin: 1.2rem auto 0.4rem auto;
    }
    .hud-ring { position: absolute; border-radius: 50%; }
    .hud-ring-a {
        inset: 0;
        border: 1px dashed rgba(201, 154, 134, 0.75);
        animation: spin 70s linear infinite;
    }
    .hud-ring-b {
        inset: 16px;
        border: 1px solid transparent;
        border-top-color: var(--rose-gold);
        border-bottom-color: var(--rose-gold);
        animation: spin 28s linear infinite reverse;
    }
    .hud-ring-c {
        inset: 34px;
        border: 1px dotted rgba(217, 139, 132, 0.65);
        animation: spin 45s linear infinite;
    }
    .hud-core {
        position: absolute;
        inset: 58px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 30%, #fff 0%, #F7D5CB 42%, #E39A91 100%);
        box-shadow: 0 0 40px rgba(227, 154, 145, 0.55);
        animation: pulse 8s ease-in-out infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes pulse {
        0%, 100% { transform: scale(0.85); }
        50%      { transform: scale(1.12); }
    }
    .aurore-title {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 300;
        font-size: 3.8rem;
        letter-spacing: 0.45em;
        padding-left: 0.45em;
        text-shadow: 0 0 28px rgba(217, 139, 132, 0.45);
        line-height: 1.1;
    }
    .aurore-subtitle {
        font-family: 'DM Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        margin: 0.6rem 0 1.6rem 0;
    }

    /* ---------- Panneaux HUD (coins en équerre) ---------- */
    .hud-panel,
    [data-testid="stChatMessage"] {
        position: relative;
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(201, 154, 134, 0.3);
        border-radius: 3px;
        padding: 14px 18px;
        margin-bottom: 12px;
        animation: rise 0.7s ease-out;
    }
    .hud-panel::before,
    [data-testid="stChatMessage"]::before {
        content: "";
        position: absolute;
        inset: -1px;
        pointer-events: none;
        background:
            linear-gradient(var(--rose-gold), var(--rose-gold)) top left / 16px 1px no-repeat,
            linear-gradient(var(--rose-gold), var(--rose-gold)) top left / 1px 16px no-repeat,
            linear-gradient(var(--rose-gold), var(--rose-gold)) top right / 16px 1px no-repeat,
            linear-gradient(var(--rose-gold), var(--rose-gold)) top right / 1px 16px no-repeat,
            linear-gradient(var(--rose-gold), var(--rose-gold)) bottom left / 16px 1px no-repeat,
            linear-gradient(var(--rose-gold), var(--rose-gold)) bottom left / 1px 16px no-repeat,
            linear-gradient(var(--rose-gold), var(--rose-gold)) bottom right / 16px 1px no-repeat,
            linear-gradient(var(--rose-gold), var(--rose-gold)) bottom right / 1px 16px no-repeat;
    }
    @keyframes rise {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: none; }
    }
    /* Messages de l'utilisateur : à droite, teintés pêche */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: rgba(242, 201, 187, 0.4);
        margin-left: 12%;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        margin-right: 12%;
    }
    [data-testid^="stChatMessageAvatar"] {
        background: linear-gradient(135deg, #F2C9BB, #D98B84) !important;
        color: var(--charcoal) !important;
    }
    .welcome p {
        margin: 0;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.35rem;
    }
    .hud-label {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-family: 'DM Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        margin: 1.2rem 0 0.6rem 0;
    }
    .hud-label::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, var(--rose-gold), transparent);
    }
    /* Libellés gris : placés après la règle générale pour la remplacer */
    .hud-label,
    .aurore-subtitle {
        color: var(--ash) !important;
    }

    /* ---------- Barre latérale ---------- */
    [data-testid="stSidebar"] {
        background: rgba(251, 244, 238, 0.72) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(201, 154, 134, 0.35);
    }

    /* ---------- Boutons ---------- */
    .stButton > button {
        width: 100%;
        background: transparent;
        border: 1px solid var(--rose-gold);
        border-radius: 2px;
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        padding: 0.65rem 1rem;
        transition: all 0.5s ease;
    }
    .stButton > button,
    .stButton > button * {
        color: var(--charcoal) !important;
    }
    .stButton > button:hover {
        background: rgba(242, 201, 187, 0.55);
        border-color: var(--rose);
        box-shadow: 0 0 22px rgba(217, 139, 132, 0.4);
    }

    /* ---------- Zone de saisie ---------- */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }
    /* La barre elle-même : fond clair, bordure rose doré */
    [data-testid="stChatInput"] {
        background: #FFFBF7 !important;
        border: 1px solid var(--rose-gold) !important;
        border-radius: 24px !important;
        box-shadow: none !important;
        transition: box-shadow 0.6s ease;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--rose) !important;
        box-shadow: 0 0 30px rgba(217, 139, 132, 0.4) !important;
    }
    /* Tous les éléments internes : plus aucun fond sombre ni bordure rouge */
    [data-testid="stChatInput"] * {
        background-color: transparent !important;
        border-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }
    /* Texte saisi, curseur et texte d'aide */
    [data-testid="stChatInput"] textarea {
        color: var(--charcoal) !important;
        -webkit-text-fill-color: var(--charcoal) !important;
        caret-color: var(--rose) !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--ash) !important;
        -webkit-text-fill-color: var(--ash) !important;
        font-style: italic;
        opacity: 1;
    }
    /* Icônes (+ et micro) */
    [data-testid="stChatInput"] button,
    [data-testid="stChatInput"] svg {
        color: var(--charcoal) !important;
        fill: var(--charcoal) !important;
    }
    /* Bouton d'envoi : rose avec flèche foncée */
    [data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"] {
        background-color: var(--peach) !important;
        border-radius: 50% !important;
    }
    [data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"]:hover {
        background-color: var(--rose) !important;
    }

    @media (prefers-reduced-motion: reduce) {
        * { animation: none !important; }
    }
</style>
"""

PETALS_HTML = '<div class="petals">' + "".join(
    f'<span class="petal" style="left:{(i * 37) % 100}%;'
    f'--s:{9 + (i * 5) % 9}px;--dx:{(i % 5) * 3 - 6}vw;'
    f'animation-duration:{26 + (i * 7) % 18}s;'
    f'animation-delay:-{(i * 4) % 30}s"></span>'
    for i in range(16)
) + "</div>"

HEADER_HTML = """
<div class="hud-header">
<div class="hud-orb">
<span class="hud-ring hud-ring-a"></span>
<span class="hud-ring hud-ring-b"></span>
<span class="hud-ring hud-ring-c"></span>
<span class="hud-core"></span>
</div>
<div class="aurore-title">AURORE</div>
<p class="aurore-subtitle">A Unique Real Organisation Running Events</p>
</div>
"""

# Horloge et date en direct, affichées dans la barre latérale.
CLOCK_WIDGET_HTML = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300&family=DM+Mono:wght@300;400&display=swap');
    html, body { margin: 0; padding: 0; background: transparent; text-align: center; color: #3B3533; }
    #clock { font-family: 'Cormorant Garamond', serif; font-weight: 300; font-size: 38px; letter-spacing: 0.18em; margin-top: 4px; }
    #date { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.3em; text-transform: uppercase; color: #6E6561; margin-top: 2px; }
</style>

<div id="clock">--:--</div>
<div id="date"></div>

<script>
    function tick() {
        const now = new Date();
        document.getElementById('clock').textContent =
            now.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
        document.getElementById('date').textContent =
            now.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });
    }
    tick();
    setInterval(tick, 1000);
</script>
"""