import streamlit as st
from datetime import datetime

# Set page config
st.set_page_config(layout="wide", page_title="Learning Hub")

st.title("Reading Corner")

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Card styling */
    .lesson-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        border-left: 5px solid #ff4b4b;
    }
    
    /* Progress indicator */
    .progress-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 10px;
    }
    
    /* Lesson title */
    .lesson-title {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
        color: #0f1215;
    }
    
    /* Tags styling */
    .tag {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 15px;
        font-size: 12px;
        margin-right: 5px;
        background-color: #f0f2f6;
        color: #0f1215;
    }
    
    /* Meta information */
    .meta-info {
        font-size: 14px;
        color: #666;
        margin: 5px 0;
    }
    
    /* Section headers */
    .section-header {
        font-size: 28px;
        font-weight: bold;
        margin: 20px 0;
        color: #0f1215;
        border-bottom: 2px solid #ff4b4b;
        padding-bottom: 10px;
    }

    /* Button container */
    .button-container {
        display: flex;
        gap: 10px;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #eee;
    }

    /* Custom button styling */
    .custom-button {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        border-radius: 5px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .primary-button {
        background-color: #ff4b4b;
        color: white;
        border: none;
    }

    .secondary-button {
        background-color: #f0f2f6;
        color: #0f1215;
        border: 1px solid #ddd;
    }

    .primary-button:hover {
        background-color: #ff3333;
    }

    .secondary-button:hover {
        background-color: #e1e4e8;
    }
    </style>
""", unsafe_allow_html=True)

# Sample lesson data - in practice, this would come from a database
lessons = [
    {
        "title": "Guide: Setting A Safe Spend Limit",
        "description": "Learn the fundamentals of data analysis using Python and popular libraries.",
        "duration": "45 mins",
        "difficulty": "Beginner",
        "tags": ["Python", "Data Analysis", "Pandas"],
        "progress": 0,
        "date": "2024-11-15",
        "author": "Sarah Johnson"
    },
    {
        "title": "Understanding Risk",
        "description": "Deep dive into sophisticated trading strategies and risk management techniques.",
        "duration": "60 mins",
        "difficulty": "Advanced",
        "tags": ["Trading", "Risk Management", "Strategy"],
        "progress": 30,
        "date": "2024-11-16",
        "author": "Michael Chen"
    },
    {
        "title": "How to Navigate the Platform",
        "description": "Understanding market trends, patterns, and analysis techniques.",
        "duration": "30 mins",
        "difficulty": "Intermediate",
        "tags": ["Markets", "Analysis", "Trends"],
        "progress": 100,
        "date": "2024-11-17",
        "author": "Alex Rivera"
    }
]

# Header section
st.markdown("<h1 style='text-align: center; color: #0f1215;'>📚 Learning Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Expand your knowledge with our comprehensive lessons</p>", unsafe_allow_html=True)

# Search and filter section
col1, col2, col3 = st.columns([2,1,1])
with col1:
    search = st.text_input("🔍 Search lessons", placeholder="Enter keywords...")
with col2:
    difficulty = st.selectbox("Difficulty", ["All Levels", "Beginner", "Intermediate", "Advanced"])
with col3:
    sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Progress"])

# Featured section
st.markdown("<div class='section-header'>Featured Lessons</div>", unsafe_allow_html=True)

# Function to render a lesson card
def render_lesson_card(lesson):
    progress_color = "green" if lesson["progress"] == 100 else "orange" if lesson["progress"] > 0 else "gray"
    progress_text = "Completed" if lesson["progress"] == 100 else f"In Progress ({lesson['progress']}%)" if lesson["progress"] > 0 else "Not Started"
    
    card_html = f"""
        <div class="lesson-card">
            <div>
                <span class="progress-badge" style="background-color: {progress_color}; color: white;">{progress_text}</span>
                <span class="meta-info">📚 {lesson['duration']} • 🎯 {lesson['difficulty']}</span>
            </div>
            <div class="lesson-title">{lesson['title']}</div>
            <div style="margin: 10px 0;">{lesson['description']}</div>
            <div>
                {"".join([f'<span class="tag">#{tag}</span>' for tag in lesson['tags']])}
            </div>
            <div class="meta-info" style="margin-top: 15px;">
                ✍️ {lesson['author']} • 📅 {lesson['date']}
            </div>
            <div class="button-container">
                <button class="custom-button primary-button" onclick="startLesson('{lesson['title']}')">
                    Start Lesson
                </button>
                <button class="custom-button secondary-button" onclick="downloadMaterials('{lesson['title']}')">
                    Download Materials
                </button>
            </div>
        </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

# Render all lesson cards
for lesson in lessons:
    render_lesson_card(lesson)
    st.markdown("---")

# Pagination
col1, col2, col3 = st.columns([2,1,2])
with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <span style='margin: 0 10px;'>Page 1 of 1</span>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>New lessons are added weekly. Stay tuned for more content!</p>
    </div>
""", unsafe_allow_html=True)

# Add JavaScript for button functionality
st.markdown("""
<script>
function startLesson(title) {
    // Handle lesson start
    console.log('Starting lesson:', title);
}

function downloadMaterials(title) {
    // Handle materials download
    console.log('Downloading materials for:', title);
}
</script>
""", unsafe_allow_html=True)