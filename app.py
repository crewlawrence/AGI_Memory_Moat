import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="AGI Memory System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .memory-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .stat-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'memories' not in st.session_state:
    st.session_state.memories = []
if 'memory_file' not in st.session_state:
    st.session_state.memory_file = 'memories.json'

# Helper functions
def load_memories(filepath):
    """Load memories from JSON file"""
    try:
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading memories: {e}")
    return []

def save_memories(memories, filepath):
    """Save memories to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(memories, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving memories: {e}")
        return False

def add_memory(content, category, tags):
    """Add a new memory"""
    memory = {
        'id': len(st.session_state.memories) + 1,
        'content': content,
        'category': category,
        'tags': tags,
        'timestamp': datetime.now().isoformat(),
        'importance': 'medium'
    }
    st.session_state.memories.append(memory)
    return memory

def search_memories(query, memories):
    """Search memories by query string"""
    if not query:
        return memories
    
    query = query.lower()
    results = []
    for mem in memories:
        if (query in mem['content'].lower() or 
            query in mem['category'].lower() or 
            any(query in tag.lower() for tag in mem['tags'])):
            results.append(mem)
    return results

# Sidebar
with st.sidebar:
    st.markdown("### 🧠 Memory System")
    
    # File management
    st.markdown("#### File Management")
    memory_file = st.text_input("Memory File", value=st.session_state.memory_file)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Load", use_container_width=True):
            st.session_state.memory_file = memory_file
            st.session_state.memories = load_memories(memory_file)
            st.success(f"Loaded {len(st.session_state.memories)} memories")
    
    with col2:
        if st.button(" Save", use_container_width=True):
            if save_memories(st.session_state.memories, memory_file):
                st.success("Memories saved!")
    
    st.divider()
    
    # Statistics
    st.markdown("#### Statistics")
    total_memories = len(st.session_state.memories)
    
    st.markdown(f"""
    <div class="stat-box">
        <h3>{total_memories}</h3>
        <p>Total Memories</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.memories:
        categories = {}
        for mem in st.session_state.memories:
            cat = mem['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        st.markdown("**By Category:**")
        for cat, count in categories.items():
            st.write(f"• {cat}: {count}")
    
    st.divider()
    
    # Filters
    st.markdown("#### Filters")
    filter_category = st.selectbox(
        "Category",
        ["All"] + list(set(mem['category'] for mem in st.session_state.memories))
    )
    
    filter_importance = st.multiselect(
        "Importance",
        ["low", "medium", "high"],
        default=["low", "medium", "high"]
    )

# Main content
st.markdown('<div class="main-header"> AGI Memory System</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Add Memory", "🔍 Search & View", "⚙️ Management"])

# Tab 1: Add Memory
with tab1:
    st.subheader("Add New Memory")
    
    with st.form("add_memory_form"):
        memory_content = st.text_area("Memory Content", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            memory_category = st.selectbox(
                "Category",
                ["Knowledge", "Experience", "Task", "Insight", "Conversation", "Other"]
            )
        
        with col2:
            memory_tags = st.text_input("Tags (comma-separated)", placeholder="ai, learning, important")
        
        submitted = st.form_submit_button("Add Memory", use_container_width=True)
        
        if submitted and memory_content:
            tags_list = [tag.strip() for tag in memory_tags.split(',') if tag.strip()]
            new_memory = add_memory(memory_content, memory_category, tags_list)
            st.success("✅ Memory added successfully!")
            st.json(new_memory)

# Tab 2: Search & View
with tab2:
    st.subheader("Search and View Memories")
    
    search_query = st.text_input("🔍 Search memories", placeholder="Enter keywords...")
    
    # Apply filters
    filtered_memories = st.session_state.memories
    
    if filter_category != "All":
        filtered_memories = [m for m in filtered_memories if m['category'] == filter_category]
    
    filtered_memories = [m for m in filtered_memories if m.get('importance', 'medium') in filter_importance]
    
    # Apply search
    if search_query:
        filtered_memories = search_memories(search_query, filtered_memories)
    
    st.write(f"**Showing {len(filtered_memories)} memories**")
    
    # Display memories
    if filtered_memories:
        for idx, memory in enumerate(reversed(filtered_memories)):
            with st.expander(f"Memory #{memory['id']} - {memory['category']} - {memory['timestamp'][:10]}"):
                st.markdown(f"**Content:** {memory['content']}")
                st.markdown(f"**Category:** {memory['category']}")
                st.markdown(f"**Tags:** {', '.join(memory['tags'])}")
                st.markdown(f"**Timestamp:** {memory['timestamp']}")
                st.markdown(f"**Importance:** {memory.get('importance', 'medium')}")
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("🗑️ Delete", key=f"del_{memory['id']}"):
                        st.session_state.memories = [m for m in st.session_state.memories if m['id'] != memory['id']]
                        st.rerun()
    else:
        st.info("No memories found. Add some memories to get started!")

# Tab 3: Management
with tab3:
    st.subheader("Memory Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Bulk Operations")
        
        if st.button("🗑️ Clear All Memories", type="secondary"):
            if st.checkbox("Confirm deletion"):
                st.session_state.memories = []
                st.success("All memories cleared!")
                st.rerun()
        
        if st.button("📤 Export to JSON"):
            json_str = json.dumps(st.session_state.memories, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"memories_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("#### Import Memories")
        uploaded_file = st.file_uploader("Upload JSON file", type=['json'])
        
        if uploaded_file is not None:
            try:
                imported_memories = json.load(uploaded_file)
                if st.button("Import Memories"):
                    st.session_state.memories.extend(imported_memories)
                    st.success(f"Imported {len(imported_memories)} memories!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error importing file: {e}")
    
    st.divider()
    
    # View all memories as JSON
    if st.checkbox("Show Raw JSON Data"):
        st.json(st.session_state.memories)
