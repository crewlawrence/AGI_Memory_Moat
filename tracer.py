import logging
import json

logging.basicConfig(filename='logs/traces.log', level=logging.INFO)

class Tracer:
    def __init__(self):
        self.trace_id = 0

    def log_decision(self, step, decision, rationale):
        self.trace_id += 1
        log_entry = {"id": self.trace_id, "step": step, "decision": decision, "rationale": rationale}
        logging.info(json.dumps(log_entry))
        return log_entry  # For chaining