import streamlit as st
import sys
from pathlib import Path
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis_core.config import DB_PATH, PROFILE_PATH
from jarvis_core.database import DatabaseManager

# Page config
st.set_page_config(
    page_title="JARVIS RPG Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 JARVIS RPG Dashboard")
st.markdown("### Personal DevOps Assistant - RPG Stats")

# Initialize database
@st.cache_resource
def get_db():
    return DatabaseManager(str(DB_PATH))

db = get_db()

# Sidebar
st.sidebar.header("⚙️ Settings")
refresh = st.sidebar.button("🔄 Refresh Data")

# Main dashboard
col1, col2, col3 = st.columns(3)

# Get user profile
try:
    profile = db.get_user_profile()
    
    with col1:
        st.metric(
            label="👤 Level",
            value=profile.get('level', 1),
            delta=None
        )
    
    with col2:
        st.metric(
            label="⭐ Experience Points",
            value=f"{profile.get('xp', 0)} XP",
            delta=None
        )
    
    with col3:
        st.metric(
            label="❤️ Health Points",
            value=f"{profile.get('hp', 100)} HP",
            delta=None
        )
    
    # XP Progress Bar
    st.markdown("### 📊 Level Progress")
    current_xp = profile.get('xp', 0)
    level = profile.get('level', 1)
    xp_needed = int((level ** 1.5) * 100)
    
    progress = min(current_xp / xp_needed, 1.0) if xp_needed > 0 else 0
    st.progress(progress)
    st.caption(f"XP: {current_xp}/{xp_needed} ({int(progress*100)}%)")
    
except Exception as e:
    st.error(f"Error loading profile: {e}")

# Vocabulary Stats
st.markdown("---")
st.markdown("### 📚 Vocabulary Statistics")

try:
    # Get vocab data
    with db._get_connection() as conn:
        # Total vocab
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vocab")
        total_vocab = cursor.fetchone()[0]
        
        # Mastery levels
        cursor.execute("""
            SELECT learning_level, COUNT(*) as count 
            FROM vocab 
            GROUP BY learning_level
            ORDER BY learning_level
        """)
        mastery_data = cursor.fetchall()
        
        # Recent vocab
        cursor.execute("""
            SELECT word, meaning, created_at, learning_level
            FROM vocab 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        recent_vocab = cursor.fetchall()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📖 Total Vocabulary", total_vocab)
        
        # Mastery distribution
        if mastery_data:
            df_mastery = pd.DataFrame(mastery_data, columns=['Level', 'Count'])
            fig = px.pie(
                df_mastery, 
                values='Count', 
                names='Level',
                title='Mastery Distribution',
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🆕 Recent Vocabulary")
        if recent_vocab:
            for word, meaning, created, level in recent_vocab[:5]:
                with st.expander(f"**{word}** (Level {level})"):
                    st.write(f"**Meaning:** {meaning}")
                    st.caption(f"Added: {created}")
        else:
            st.info("No vocabulary yet. Start learning!")

except Exception as e:
    st.error(f"Error loading vocabulary stats: {e}")

# Activity Timeline
st.markdown("---")
st.markdown("### 📈 Learning Activity")

try:
    with db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM vocab
            WHERE created_at IS NOT NULL
            GROUP BY DATE(created_at)
            ORDER BY date DESC
            LIMIT 30
        """)
        activity_data = cursor.fetchall()
        
        if activity_data:
            df_activity = pd.DataFrame(activity_data, columns=['Date', 'Words Learned'])
            df_activity['Date'] = pd.to_datetime(df_activity['Date'])
            
            fig = px.bar(
                df_activity.sort_values('Date'),
                x='Date',
                y='Words Learned',
                title='Vocabulary Learning Activity (Last 30 Days)',
                color='Words Learned',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No activity data yet. Start your learning journey!")
            
except Exception as e:
    st.error(f"Error loading activity timeline: {e}")

# Footer
st.markdown("---")
st.caption("🤖 JARVIS RPG Assistant | Powered by Streamlit")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
