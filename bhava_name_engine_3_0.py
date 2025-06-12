import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io
import uuid

# --- Bhāva Name Engine Functions ---
PHONEMES = sorted([
    'kha', 'gha', 'cha', 'jha', 'ṭha', 'ḍha', 'tha', 'dha', 'pha', 'bha',
    'ka', 'ga', 'ca', 'ja', 'ṭa', 'ḍa', 'ta', 'da', 'pa', 'ba',
    'ṅa', 'ña', 'ṇa', 'na', 'ma',
    'ya', 'ra', 'la', 'va',
    'śa', 'ṣa', 'sa', 'ha',
    'a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'ai', 'o', 'au', 'ṁ', 'ḥ'
], key=len, reverse=True)

PHONEME_BHAVA_MAP = {
    'ka': ('Jñāna (Wisdom)', 'Ājñā', 'Adbhuta (Wonder)', '#2980b9'),
    'ma': ('Śāntiḥ (Peace)', 'Sahasrāra', 'Śānta (Tranquility)', '#95a5a6'),
    'ra': ('Vīraḥ (Heroism)', 'Mūlādhāra', 'Vīra (Courage)', '#e74c3c'),
    'na': ('Karunā (Compassion)', 'Anāhata', 'Karuṇā (Compassion)', '#2ecc71'),
    'ya': ('Ānanda (Bliss)', 'Sahasrāra', 'Hāsya (Joy)', '#f39c12'),
    'bha': ('Vikāsa (Expansion)', 'Sahasrāra', 'Adbhuta (Amazement)', '#9b59b6'),
    'ta': ('Dhairya (Courage)', 'Maṇipūra', 'Vīra (Heroism)', '#f39c12'),
    'sa': ('Dharma (Righteousness)', 'Viśuddha', 'Vīra (Justice)', '#3498db'),
    'la': ('Prema (Love)', 'Anāhata', 'Śṛṅgāra (Beauty)', '#ff7675'),
    'ha': ('Mokṣa (Liberation)', 'Sahasrāra', 'Śānta (Transcendence)', '#9b59b6'),
    'a': ('Satya (Truth)', 'All', 'Śānta (Calm)', '#ecf0f1'),
    'i': ('Medhā (Intellect)', 'Ājñā', 'Adbhuta (Wisdom)', '#3498db'),
}

def parse_syllables(name: str):
    name = name.lower().strip().replace('ṃ', 'ṁ')
    syllables = []
    while name:
        match = next((p for p in PHONEMES if name.startswith(p)), None)
        if match:
            syllables.append(match)
            name = name[len(match):]
        else:
            name = name[1:]
    return syllables

def guess_phoneme(syll: str):
    for key in PHONEME_BHAVA_MAP:
        if syll in key or key in syll or syll[0] == key[0]:
            return PHONEME_BHAVA_MAP[key]
    return None

def guess_bhava_tags(name: str):
    syllables = parse_syllables(name)
    matched = [PHONEME_BHAVA_MAP[s] for s in syllables if s in PHONEME_BHAVA_MAP]
    guessed = [guess_phoneme(s) for s in syllables if s not in PHONEME_BHAVA_MAP]
    guessed = [g for g in guessed if g]
    return list(set(matched + guessed))

def generate_bhava_card(name: str, tags: list):
    width = 720
    height = 120 * len(tags) + 100
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_body = ImageFont.truetype("arial.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
    draw.text((20, 20), f"Bhāva Profile: {name}", fill="black", font=font_title)
    y = 80
    for bhava, chakra, rasa, color in tags:
        draw.rectangle([(20, y), (width - 20, y + 80)], fill=color)
        draw.text((40, y + 25), f"{chakra} • {bhava} • {rasa}", fill="white", font=font_body)
        y += 100
    return img

def get_card_png_bytes(name: str, tags: list):
    img = generate_bhava_card(name, tags)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# --- Chakra–Deva Explorer Data ---
deva_data = [
    {"Deva": "🌊 Varuṇa", "Type": "☀️ Āditya", "Chakra": "🟦 Viśuddha", "Element": "💧 Water", "Vāhana": "🐊 Makara", "Bīja": "🕉️ Om Vam Varuṇāya Namaḥ"},
    {"Deva": "🌞 Mitra", "Type": "☀️ Āditya", "Chakra": "💚 Anāhata", "Element": "🔆 Solar", "Vāhana": "🐎 Horse", "Bīja": "-"},
    {"Deva": "🛡️ Āryaman", "Type": "☀️ Āditya", "Chakra": "🟡 Maṇipūra", "Element": "🌞 Solar Dignity", "Vāhana": "-", "Bīja": "-"},
    {"Deva": "💰 Bhaga", "Type": "☀️ Āditya", "Chakra": "🧡 Svādhiṣṭhāna", "Element": "🪙 Abundance", "Vāhana": "🦁 Lion", "Bīja": "🕉️ Om Bhagāya Namaḥ"},
    {"Deva": "🌗 Aṃśa", "Type": "☀️ Āditya", "Chakra": "🟣 Ājñā", "Element": "🥛 Soma-share", "Vāhana": "-", "Bīja": "-"},
    {"Deva": "🛠️ Tvaṣṭṛ", "Type": "☀️ Āditya", "Chakra": "🔴 Mūlādhāra", "Element": "🧱 Creation", "Vāhana": "🐘 Elephant", "Bīja": "🕉️ Om Tvaṣṭre Namaḥ"},
    {"Deva": "☀️ Savitṛ", "Type": "☀️ Āditya", "Chakra": "⚪ Sahasrāra", "Element": "🌅 Solar Radiance", "Vāhana": "🌟 Golden Chariot", "Bīja": "🕉️ Tat Savitur Vareṇyam..."},
    {"Deva": "🧭 Pūṣan", "Type": "☀️ Āditya", "Chakra": "🟣 Ājñā", "Element": "🛤️ Guidance", "Vāhana": "🐐 Goat", "Bīja": "🕉️ Om Pūṣṇe Namaḥ"},
    {"Deva": "📏 Dakṣa", "Type": "☀️ Āditya", "Chakra": "🟣 Ājñā", "Element": "📐 Order", "Vāhana": "🦁 Lion", "Bīja": "🕉️ Om Dakṣāya Namaḥ"},
    {"Deva": "☀️ Vivasvān", "Type": "☀️ Āditya", "Chakra": "⚪ Sahasrāra", "Element": "🔆 Light", "Vāhana": "🐎 Seven-Horse Chariot", "Bīja": "🕉️ Om Sūryāya Namaḥ"},
    {"Deva": "⚡ Indra", "Type": "☀️ Āditya", "Chakra": "🟡 Maṇipūra", "Element": "🔥 Energy", "Vāhana": "🐘 Airāvata", "Bīja": "🕉️ Om Indrāya Namaḥ"},
    {"Deva": "🛡️ Viṣṇu", "Type": "☀️ Āditya", "Chakra": "🌈 All", "Element": "🛡️ Preserver", "Vāhana": "🦅 Garuḍa", "Bīja": "🕉️ Om Namo Nārāyaṇāya"},
    {"Deva": "🔱 Śiva", "Type": "🌪️ Rudra", "Chakra": "🟣 Ājñā", "Element": "🌀 Destruction/Transformation", "Vāhana": "🐂 Bull (Nandi)", "Bīja": "🕉️ Om Namaḥ Śivāya"},
    {"Deva": "🔥 Manyu", "Type": "🌪️ Rudra", "Chakra": "🟡 Maṇipūra", "Element": "😠 Anger", "Vāhana": "🦁 Lion", "Bīja": "🕉️ Om Manyave Namaḥ"},
    {"Deva": "🐯 Ugra", "Type": "🌪️ Rudra", "Chakra": "🔴 Mūlādhāra", "Element": "💪 Fierce Will", "Vāhana": "🐅 Tiger", "Bīja": "🕉️ Om Ugrāya Namaḥ"},
    {"Deva": "📣 Bhīma", "Type": "🌪️ Rudra", "Chakra": "🟦 Viśuddha", "Element": "📢 Roar", "Vāhana": "🐘 Elephant", "Bīja": "-"},
    {"Deva": "🌀 Kapardī", "Type": "🌪️ Rudra", "Chakra": "⚪ Sahasrāra", "Element": "🔥 Tapas", "Vāhana": "🐂 Bull", "Bīja": "-"},
    {"Deva": "🌟 Raivata", "Type": "🌪️ Rudra", "Chakra": "🟣 Ājñā", "Element": "✨ Radiance", "Vāhana": "🦌 Deer", "Bīja": "-"},
    {"Deva": "🐍 Sarpī", "Type": "🌪️ Rudra", "Chakra": "🔴 Mūlādhāra", "Element": "🐉 Kundalinī", "Vāhana": "🐍 Serpent", "Bīja": "🕉️ Saṃ"},
    {"Deva": "⚡ Vijra", "Type": "🌪️ Rudra", "Chakra": "🟣 Ājñā", "Element": "🎯 Focus", "Vāhana": "🦅 Lightning Bird", "Bīja": "-"},
    {"Deva": "🌩️ Āśani", "Type": "🌪️ Rudra", "Chakra": "🟣 Ājñā", "Element": "⚡ Thunderbolt", "Vāhana": "☁️ Thundercloud", "Bīja": "-"},
    {"Deva": "🌌 Mahān", "Type": "🌪️ Rudra", "Chakra": "⚪ Sahasrāra", "Element": "🌠 Greatness", "Vāhana": "🌠 Cosmic Mount", "Bīja": "-"},
    {"Deva": "🌿 Ṛtudhvaja", "Type": "🌪️ Rudra", "Chakra": "🧡 Svādhiṣṭhāna", "Element": "🌸 Cycle/Season", "Vāhana": "🛞 Chariot of Seasons", "Bīja": "-"},
    {"Deva": "🌊 Āpaḥ", "Type": "🪨 Vasu", "Chakra": "🧡 Svādhiṣṭhāna", "Element": "💧 Water", "Vāhana": "🐢 Turtle", "Bīja": "🕉️ Om Āpaḥ Svaḥ"},
    {"Deva": "🧭 Dhruva", "Type": "🪨 Vasu", "Chakra": "⚪ Sahasrāra", "Element": "🧘 Stillness", "Vāhana": "🌌", "Bīja": "🪷 Dhruva Stuti"},
    {"Deva": "🌙 Soma", "Type": "🪨 Vasu", "Chakra": "🟣 Ājñā", "Element": "🥛 Moon Nectar", "Vāhana": "🦌 Deer", "Bīja": "🕉️ Om Somāya Namaḥ"},
    {"Deva": "🌍 Dhara", "Type": "🪨 Vasu", "Chakra": "🔴 Mūlādhāra", "Element": "🌎 Earth", "Vāhana": "🐘 Elephant", "Bīja": "🕉️ Om Dhārayantyai Namaḥ"},
    {"Deva": "💨 Anila", "Type": "🪨 Vasu", "Chakra": "💚 Anāhata", "Element": "🌬️ Air", "Vāhana": "🦌 Deer", "Bīja": "🕉️ Om Anilāya Namaḥ"},
    {"Deva": "🔥 Anala", "Type": "🪨 Vasu", "Chakra": "🟡 Maṇipūra", "Element": "🔥 Fire", "Vāhana": "🐏 Ram", "Bīja": "🕉️ Om Agnaye Namaḥ"},
    {"Deva": "🌅 Pratyūṣa", "Type": "🪨 Vasu", "Chakra": "🟦 Viśuddha", "Element": "🌄 Dawn", "Vāhana": "🐎 Golden Horse", "Bīja": "-"},
    {"Deva": "💡 Prabhāsa", "Type": "🪨 Vasu", "Chakra": "⚪ Sahasrāra", "Element": "💫 Radiance", "Vāhana": "🦚 Peacock", "Bīja": "∞"},
    {"Deva": "🌬️ Nāṣatya", "Type": "👬 Aśvin", "Chakra": "🦗 Iḍā", "Element": "🌬️ Breath (Left)", "Vāhana": "🐎 Horse", "Bīja": "🕉️ Om Nāsatye Namaḥ"},
    {"Deva": "💪 Dasra", "Type": "👬 Aśvin", "Chakra": "🔥 Piṅgalā", "Element": "🔋 Vitality (Right)", "Vāhana": "🐎 Horse", "Bīja": "🕉️ Om Dasrāya Namaḥ"},
]

deva_df = pd.DataFrame(deva_data)

# --- Siddhi Skill Web Data ---
siddhis = [
    {"name": "Mahimā", "chakra": "Sahasrāra", "color": "#6A0DAD", "icon": "🕉️", "desc": "Cosmic Expansion"},
    {"name": "Īśitva", "chakra": "Maṇipūra", "color": "#FF6F00", "icon": "🔥", "desc": "Elemental Control"},
    {"name": "Vaśitva", "chakra": "Viśuddha", "color": "#3F51B5", "icon": "🔊", "desc": "Mastery Over Minds"},
    {"name": "Laghimā", "chakra": "Ājñā", "color": "#00ACC1", "icon": "👁️", "desc": "Levitation & Speed"},
    {"name": "Aṇimā", "chakra": "Mūlādhāra", "color": "#4CAF50", "icon": "🪷", "desc": "Micro-Size Ability"},
    {"name": "Garimā", "chakra": "Svādhiṣṭhāna", "color": "#795548", "icon": "💧", "desc": "Infinite Weight"},
    {"name": "Prāpti", "chakra": "Anāhata", "color": "#FFC107", "icon": "💫", "desc": "Reach Anything"},
    {"name": "Prākāmya", "chakra": "Sahasrāra", "color": "#E91E63", "icon": "🌈", "desc": "Will Become Reality"},
]

sadhana_cards = {
    "Mahimā": {
        "practice": "Meditate on infinite space (ākāśa) with breath expansion, visualizing the cosmos within.",
        "mantra": "ॐ महिमा सिद्धये नमः (Om Mahimā Siddhaye Namaḥ)",
        "ritual": "Offer Arghya (water libation) to the Sun facing East at dawn.",
        "scripture": "Yoga Sūtra III.45 — Mastery over elements leads to Mahimā.",
        "benefits": "Expands consciousness, dissolves ego, awakens cosmic unity."
    },
    "Īśitva": {
        "practice": "Chant Panchabhūta mantras while mentally commanding elemental energies with intent.",
        "mantra": "ॐ ईशित्व सिद्धये नमः (Om Īśitva Siddhaye Namaḥ)",
        "ritual": "Light five elemental lamps during new moon and meditate on their unity.",
        "scripture": "Śrīmad Bhāgavatam 11.15.17 — Lord Kṛṣṇa reveals Siddhis to Uddhava.",
        "benefits": "Grants authority over elemental patterns, deepens yogic sovereignty."
    },
    "Vaśitva": {
        "practice": "Silent japa while visualizing blue flame in throat; speak only truth that uplifts.",
        "mantra": "ॐ वशित्व सिद्धये नमः (Om Vaśitva Siddhaye Namaḥ)",
        "ritual": "Offer fragrant flowers or incense at dawn while reciting the Sarasvatī Stotra.",
        "scripture": "Tantra Sāra — Mastery over speech and minds is Vaśitva.",
        "benefits": "Inspires natural charisma, spiritual persuasion, and vocal purity."
    },
    "Laghimā": {
        "practice": "Practice Trāṭaka on the rising sun, visualizing lightness and speed of light within.",
        "mantra": "ॐ लघिमा सिद्धये नमः (Om Laghimā Siddhaye Namaḥ)",
        "ritual": "Perform Vāyu-mudrā pranayama in the early morning breeze.",
        "scripture": "Hatha Yoga Pradīpikā III.45 — Laghimā arises from Vāyu control.",
        "benefits": "Reduces inner heaviness, fosters swiftness of thought and being."
    },
    "Aṇimā": {
        "practice": "Meditate on the bindu (point) between eyebrows shrinking into atomic subtlety.",
        "mantra": "ॐ अणिमा सिद्धये नमः (Om Aṇimā Siddhaye Namaḥ)",
        "ritual": "Perform Sūkṣma Sharīra dhyāna under moonlight.",
        "scripture": "Śiva Saṁhitā — Yogin becomes subtler than the subtlest.",
        "benefits": "Dissolves bodily identity, activates subtle perception."
    },
    "Garimā": {
        "practice": "Visualize yourself as immovable as a mountain; ground energy through slow breaths.",
        "mantra": "ॐ गरिमा सिद्धये नमः (Om Garimā Siddhaye Namaḥ)",
        "ritual": "Do bhūmi namaskāra (earth salutations) daily at dusk.",
        "scripture": "Pātañjala Yoga — One becomes heavier than all by meditating on Earth.",
        "benefits": "Builds spiritual gravitas, emotional stability, inner weight."
    },
    "Prāpti": {
        "practice": "During meditation, extend awareness to distant places or desired objects.",
        "mantra": "ॐ प्राप्ति सिद्धये नमः (Om Prāpti Siddhaye Namaḥ)",
        "ritual": "Offer sacred water to a map or globe while invoking all-directional reach.",
        "scripture": "Śrīmad Bhāgavatam 11.15.19 — One attains remote access to anything.",
        "benefits": "Enhances spiritual intuition, remote perception, energy access."
    },
    "Prākāmya": {
        "practice": "Practice sankalpa sādhanā: visualize a pure desire and let it bloom in stillness.",
        "mantra": "ॐ प्राकाम्य सिद्धये नमः (Om Prākāmya Siddhaye Namaḥ)",
        "ritual": "Write your desire on sacred ash or leaf and dissolve it in water.",
        "scripture": "Yoga Sūtra III.36 — Desire merges with reality in yogic union.",
        "benefits": "Aligns will with Dharma, manifests higher intentions instantly."
    },
}

siddhi_lore = {
    "Mahimā": "The power to expand one's consciousness and presence beyond physical dimensions—merging with the infinite.",
    "Īśitva": "Sovereignty over the elements—fire, water, air, earth—through sheer will. The Siddha becomes a cosmic commander.",
    "Vaśitva": "The ability to attract and influence the minds of others, harmonizing or dominating thought currents.",
    "Laghimā": "Transcending gravity, the yogī becomes light as thought itself, capable of levitating, flying, or vanishing.",
    "Aṇimā": "The miraculous ability to reduce one's form to the tiniest possible size, becoming subtler than the atom.",
    "Garimā": "To gain infinite mass or gravity—rooted like a mountain, immovable even by gods.",
    "Prāpti": "The Siddha can reach and touch anything in creation—remotely access places, objects, or even minds.",
    "Prākāmya": "All desires manifest instantly. No separation between intent and reality.",
}

# --- Streamlit App ---
st.set_page_config(page_title="Bhāva Name Engine 3.0 by Mahān !!!", page_icon="🕉", layout="wide")
st.title("🌸 Bhāva Name Engine 3.0")
st.markdown("Map your name to its **emotive essence**, **Chakra flow**, and **Rasa**, and explore associated **Vedic Devas** and **Siddhi powers** — powered by Sanskrit phonetics, Rasa theory, and Vedic wisdom.")

# Input Section
st.header("🔤 Enter Your Name")
name_input = st.text_input("Enter a name:", placeholder="e.g., Krishna")
if name_input:
    tags = guess_bhava_tags(name_input)
    if tags:
        # --- Bhāva-Chakra-Rasa Mapping ---
        st.subheader("✨ Bhāva-Chakra-Rasa Map")
        for bhava, chakra, rasa, color in tags:
            st.markdown(
                f"<div style='padding:10px;margin:5px;border-radius:10px;background:{color};color:white'><b>{chakra}</b> • {bhava} • <i>{rasa}</i></div>",
                unsafe_allow_html=True
            )
        png_data = get_card_png_bytes(name_input, tags)
        st.download_button(
            "📥 Download Bhāva Card (PNG)",
            data=png_data,
            file_name=f"{name_input}_bhava_card.png",
            mime="image/png"
        )

        # Extract Chakras (remove emoji prefixes for matching)
        chakras = [chakra.split(" ")[-1] if " " in chakra else chakra for _, chakra, _, _ in tags]
        chakras = list(set(chakras))  # Unique Chakras
        if "All" in chakras:
            chakras = deva_df["Chakra"].apply(lambda x: x.split(" ")[-1] if " " in x else x).unique().tolist()

        # --- Chakra–Deva Explorer ---
        st.subheader("🧘 Associated Vedic Devas")
        filtered_deva_df = deva_df[deva_df["Chakra"].apply(lambda x: x.split(" ")[-1] if " " in x else x).isin(chakras)]
        if not filtered_deva_df.empty:
            st.dataframe(filtered_deva_df, use_container_width=True)
            fig = px.bar(
                filtered_deva_df,
                x="Chakra",
                color="Deva",
                title="🔆 Devas per Chakra",
                labels={"Chakra": "Chakra Center", "Deva": "Deva Name"}
            )
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("🪔 Devotional Cards")
            for _, row in filtered_deva_df.iterrows():
                with st.expander(f"{row['Deva']} ({row['Type']}) – {row['Chakra']}"):
                    st.markdown(f"""
                    - **Element:** {row['Element']}
                    - **Vāhana:** {row['Vāhana']}
                    - **Bīja Mantra:** `{row['Bīja']}`
                    """)
        else:
            st.warning("No Devas found for the associated Chakras.")

        # --- Siddhi Skill Web ---
        st.subheader("🪬 Associated Siddhi Powers")
        filtered_siddhis = [s for s in siddhis if s["chakra"] in chakras]
        if filtered_siddhis:
            cols = st.columns(min(len(filtered_siddhis), 4))
            for i, siddhi in enumerate(filtered_siddhis):
                with cols[i % 4]:
                    label = f"{siddhi['icon']} {siddhi['name']}"
                    if st.button(label, key=f"siddhi_{siddhi['name']}_{uuid.uuid4()}"):
                        st.session_state["selected_siddhi"] = siddhi

            if "selected_siddhi" in st.session_state:
                s = st.session_state["selected_siddhi"]
                with st.expander(f"📜 {s['icon']} {s['name']} Siddhi — Tap to Expand", expanded=True):
                    st.markdown(f"### {s['icon']} {s['name']}")
                    st.markdown(f"**Chakra:** `{s['chakra']}`")
                    st.markdown(f"**Essence:** {s['desc']}")
                    lore = siddhi_lore.get(s["name"], "No lore available yet.")
                    st.markdown(f"**🧙‍♂️ Lore:** {lore}")
                    st.markdown("**Tier:** II / V")
                    st.progress(0.6)
                    s_card = sadhana_cards.get(s["name"], None)
                    if s_card:
                        st.markdown("### 🪬 Sādhanā Practice")
                        st.markdown(f"**🧘 Daily Practice:** {s_card['practice']}")
                        st.markdown(f"**🕉️ Mantra:** `{s_card['mantra']}`")
                        st.markdown(f"**📿 Ritual:** {s_card['ritual']}")
                        st.markdown(f"**📖 Scripture:** *{s_card['scripture']}*")
                        st.info(f"✨ Benefit: {s_card['benefits']}")
        else:
            st.warning("No Siddhi powers found for the associated Chakras.")
    else:
        st.warning("No Bhāva tags could be confidently inferred.")

st.markdown("---")
st.markdown("🧬 Powered by Maheshwara Sūtras • Rasa Theory • Sanskrit Sound Science • Vedic Wisdom")
