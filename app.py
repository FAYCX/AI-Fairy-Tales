import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random
import json

# Load model and tokenizer
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

st.set_page_config(
    page_title="The Mosaic Mind of AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for fonts and body
st.markdown('<style>div.block-container{padding-top:0.5rem;}</style>', unsafe_allow_html=True)

white_color = "#fff"
h1 = "1.8rem"
h2 = "1.5rem"
h3 = "1.1rem"
p = "0.9rem"

font_css = f"""
<style>
    body {{
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: black;
        color: white;
    }}
    .title-box {{
        padding: 10px;
        margin: 10px;
        background-color: #333;
        color: {white_color};
        border-radius: 10px;
        box-shadow: 0.4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }}
    h1 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h1};
        font-weight: bold;
        font-stretch: condensed;
        margin: 0;
        letter-spacing: 0.08rem;
    }}
    h2 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h2};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.02rem;
    }}
    h3 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h3};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.01rem;
        color: #edcce8;
    }}
    h5, p {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color: #85888c;
        font-size: {p};
    }}
    @media (max-width: 480px) {{
        .title-box {{
            padding: 10px;
            margin: 10px;
        }}
        h1 {{
            font-size: 1.4rem;
        }}
    }}
    h2 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h2};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.02rem;
    }}
    h3 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h3};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.01rem;
    }}
    h5, p {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color: #dbdbdb;
        font-size: {p};
    }}
</style>
"""

st.markdown(font_css, unsafe_allow_html=True)

# Function to generate text using GPT-2
def generate_text(prompt, length=300, temperature=0.65):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=length, temperature=temperature, no_repeat_ngram_size=2)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

# Load JSON data
books = json.load(open("books.json"))
celebrities = json.load(open("celebrities.json"))
president_quotes = json.load(open("president_quote.json"))

# Predefined story beginnings and keywords
Beginning = ["As the leaves started turning golden", "On a rainy Sunday", "On the eve of a great adventure", "It's the most wonderful season of the year", "Under a starlit sky", "During the last days of summer", "When the first snow began to fall", "While the town slept soundly", "On the busiest day of the year"]

genre_keywords = {
    "Fantasy": ["wizard", "spell", "dragon", "kingdom", "enchantment", "beast", "elf", "dwarf", "goblin", "unicorn", "alicorn", "phoenix", "troll", "mermaid", "magic", "alien"],
    "Horror": ["vampire", "ghost", "fear", "death", "curse","demon", "zombie", "possession", "phantom", "cult", "nightmare", "graveyard", "cemetery"],
    "Romantic": ["candlelight", "love", "heart", "romance", "passion", "kiss", "crush","desire", "honeymoon", "valentine", "wedding", "party", "date"]
}

character_traits = {
    "personality": ["curious and brave", "sweet and lovely", "lovely and gentle", "witty and sarcastic", "kind and thoughtful", "optimistic and energetic", "philosophical and introspective", "nervous and always in a hurry", "reckless and adventurous", "reserved and meticulous", "charming and persuasive", "practical and no-nonsense", "cynical and world-weary", "trusting and naive", "driven and ambitious", "creative and imaginative", "skeptical and inquisitive", "compassionate and empathetic", "haughty and arrogant", "loyal and devoted", "playful and adventurous"],
    "occupation": ["timekeeper", "gardener", "journalist", "scientist", "merchant", "scholar", "teacher", "nurse", "diplomat", "doctor", "spy", "chief", "wizard", "blacksmith", "navigator", "celebrity", "librarian", "farmer", "sailor", "philosopher", "painter", "professor", "student", "politician", "engineer"]
}

genre_words = {
    "Fantasy": ["magical", "enchanted", "serenely", "mystical"],
    "Horror": ["deadly", "scary", "ghastly", "haunting"],
    "Romantic": ["beautiful", "lovely", "romantic", "sweetly"]
}

def collect_interactions():
    with st.sidebar.form(key='interaction_form'):
        st.write("Add Character Interaction")
        source = st.text_input("Character One", help="Name of the source character.")
        target = st.text_input("Character Two", help="Name of the target character.")
        interaction_count = st.number_input("Interaction Frequency", min_value=1, max_value=100, help="How many times have these characters interacted?")
        submit_button = st.form_submit_button(label='Add Interaction')

        if submit_button:
            if 'interactions' not in st.session_state:
                st.session_state.interactions = {}
            
            interaction_key = (source, target)
            if interaction_key in st.session_state.interactions:
                st.session_state.interactions[interaction_key] += interaction_count
            else:
                st.session_state.interactions[interaction_key] = interaction_count
            
            st.success(f"Added interaction: {source} - {target} ({st.session_state.interactions[interaction_key]} times)")

def display_interactions():
    if 'interactions' in st.session_state and st.session_state.interactions:
        for (source, target), count in st.session_state.interactions.items():
            st.sidebar.write(f"{source} - {target}, {count} times")

def main():
    st.sidebar.subheader("Configure Your Story")
    genre = st.sidebar.selectbox("Genre", ["Fantasy", "Horror", "Romantic"])
    main_character = st.sidebar.text_input("Main Character", "Alice")
    secondary_character = st.sidebar.text_input("Secondary Character", "Eleanor")
    setting = st.sidebar.text_input("Place", "coffee shop")

    story_length = st.sidebar.slider("Story Length", 100, 500, 300)
    temperature = st.sidebar.slider("Creativity Temperature", 0.3, 0.9, 0.65)

    if setting == "an enchanted forest":  # Default plot message is unchanged
        st.error('Please use the left sidebar to set the parameters. Your selected genre, characters, and setting elements will actively shape the course of the story.')

    st.title("Welcome to AI Fairy Tale Box!")
    st.subheader("Where a fine-tuned GPT-2 model blends with rule-based structure")

    for _ in range(2):
            st.write("")

    st.write("Dive into the world of bespoke storytelling with our generator, crafted in two distinct parts. The first `two-thirds` of each narrative is meticulously shaped using a tracery-like grammar with a rule-based structure. It randomly weaves elements like real-world book titles, presidential quotes, and celebrity names into the fabric of the story. The `remaining third` leverages the power of the GPT-2 model to generate the rest based on the clues provided in the initial sentences. Each narrative unfolds uniquely based on the input, tailoring an experience that invites us collectively to re-examine the human and AI mind, fostering innovative storytelling through the combination of electronic text and the mathematical algorithms within the AI model.")

    if st.sidebar.button("Generate Story"):
        create_story(genre, main_character, secondary_character, setting, story_length, temperature)

def create_story(genre, main_character, secondary_character, setting, story_length, temperature):
    Begin = random.choice(Beginning)
    keywords = random.sample(genre_keywords[genre], 2)
    words = random.sample(genre_words[genre], 2)
    selected_personality = random.choice(character_traits["personality"])
    selected_occupation = random.choice(character_traits["occupation"])
    selected_book = random.choice(books)
    selected_book2 = random.choice(books)
    selected_celebrities = random.choice(celebrities)
    selected_president = random.choice(president_quotes)
    selected_name = selected_president['name']
    selected_quote = random.choice(selected_president['quotes'])
    selected_personality2 = random.choice(character_traits["personality"])
    selected_occupation2 = random.choice(character_traits["occupation"])

    prompt = f"""
{Begin}, {main_character}, a {selected_personality} {selected_occupation}, settled into a quiet nook with the book, '{selected_book}', at the most {words[0]} {setting} in town. 
Next to her, {secondary_character}, a {selected_personality2} {selected_occupation2}, was engrossed in '{selected_book2}' at the neighboring nook. 
Suddenly, a distinct voice in the distance began reciting "{selected_quote}". 
"Could that possibly be the President {selected_name}?" {main_character} mused, her gaze still fixed on her page. 
As the voice drew nearer, {main_character} finally looked up to see none other than {selected_celebrities} approaching! 
This story is all about {keywords[0]} and {keywords[1]}. 
Why was {selected_celebrities} there, and what adventures await in this {words[1]} {setting}?
"""

    story = generate_text(prompt, length=story_length, temperature=temperature)
        
    for _ in range(2):
            st.write("")
        
    st.subheader("Your Generated Story:")
    for _ in range(2):
        st.write("")

    st.markdown(f'<div class="highlight-box">{story}</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
