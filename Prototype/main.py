from agent import AGIAgent
from config import load_config  # Assume loads .env

load_config()
agent = AGIAgent()
# Seed moats
agent.memory.add_memory("Previous trip: SF to LA, avoid traffic.")
agent.data_moat.add_data("traffic_insight", {"tip": "Use I-5 after 8pm."})

# Demo loop
task = input("Enter task (e.g., Plan a trip from SF to LA): ")
result = agent.reason_loop(task)
print(f"Result: {result}")