Bhāva Name Engine 3.0
🌸 A Streamlit web application that maps a name to its emotive essence (Bhāva), Chakra, and Rasa using Sanskrit phonetics, and explores associated Vedic Devas and Siddhi powers.
Overview
The Bhāva Name Engine 3.0 is an interactive tool inspired by Sanskrit phonetics, Rasa theory, and Vedic wisdom. It takes a name as input and provides:

Bhāva-Chakra-Rasa Map: Maps the name to emotive qualities, Chakras, Rasas, and colors, with downloadable PNG cards.
Vedic Deva Explorer: Displays Vedic Devas (e.g., Varuṇa, Śiva) linked to the identified Chakras, with tables, Plotly visualizations, and devotional cards.
Siddhi Skill Web: Showcases Siddhi powers (e.g., Mahimā, Aṇimā) associated with the Chakras, including practices, mantras, and benefits.

The app is designed for spiritual enthusiasts, yogis, and those interested in Vedic and Sanskrit traditions.
Features

Input: Enter a single name to generate a personalized Bhāva profile.
Bhāva Mapping: Displays Bhāva, Chakra, Rasa, and color associations with a downloadable PNG card.
Deva Explorer: Interactive table and bar chart of Vedic Devas, with expandable devotional cards detailing elements, Vāhanas, and Bīja mantras.
Siddhi Powers: Grid of Siddhi buttons with detailed cards on practices, mantras, rituals, scriptures, and benefits.
Visuals: Emoji-enhanced UI, Plotly charts, and responsive wide layout.
Error Handling: Graceful warnings for unmapped names or missing data.

Installation

Clone the Repository:
git clone https://github.com/your-username/Bhava-Name-Engine-3.0.git
cd Bhava-Name-Engine-3.0


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Run the App:
streamlit run bhava_name_engine_3_0.py

The app will open in your default browser at http://localhost:8501.


Requirements
See requirements.txt for the full list of dependencies. Key packages include:

streamlit>=1.27.0
pandas>=2.0.0
plotly>=5.15.0
Pillow>=9.5.0

Python version: 3.8 or higher.
Usage

Open the app in your browser.
Enter a name (e.g., "Krishna") in the text input field.
View the Bhāva-Chakra-Rasa Map with colored cards and download the PNG card.
Explore the Vedic Devas section for associated Devas, including a table, bar chart, and devotional cards.
Click buttons in the Siddhi Powers section to view details on spiritual practices and benefits.
Use the wide layout and expanders for an interactive experience.

Deployment
To deploy to Streamlit Cloud:

Push the repository to GitHub.
Connect your GitHub account to Streamlit Cloud.
Select the repository and specify bhava_name_engine_3_0.py as the main file.
Ensure requirements.txt is included for dependency installation.
Deploy and share the public URL.

Notes

The app uses arial.ttf for Bhāva card generation. If unavailable, it falls back to PIL's default font.
Chakra names with emoji prefixes (e.g., "🟦 Viśuddha") are normalized for matching across datasets.
The app is self-contained, with all data embedded in the script for simplicity.

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

License
MIT License. See LICENSE for details.
Acknowledgments

Inspired by Maheshwara Sūtras, Rasa Theory, and Vedic traditions.
Built with Streamlit, Pandas, Plotly, and Pillow.

🧬 Powered by Sanskrit Sound Science and Vedic Wisdom.
