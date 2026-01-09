from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from tracer import Tracer
from memory_moat import MemoryMoat
from data_moat import DataMoat

class AGIAgent:
    def __init__(self, llm=OpenAI(), memory=MemoryMoat(), data_moat=DataMoat(), tracer=Tracer()):
        self.llm = llm
        self.memory = memory
        self.data_moat = data_moat
        self.tracer = tracer
        self.prompt = PromptTemplate(input_variables=["input", "context"], template="Task: {input}\nContext: {context}\nResponse:")

    def reason_loop(self, task, max_iters=5):
        context = ""
        for iter in range(max_iters):
            # Retrieve from moats
            mem_results = self.memory.retrieve(task)
            data_results = self.data_moat.query(task)
            context = f"Memory: {mem_results}\nData: {data_results}"

            # LLM call with loop
            chain = LLMChain(llm=self.llm, prompt=self.prompt)
            response = chain.run(input=task, context=context)

            # Trace decision
            trace = self.tracer.log_decision(f"Iter {iter}", response, f"Used context: {context[:100]}...")

            # Self-improve: Add to moats if good
            if self._evaluate(response):  # Simple eval; e.g., len(response) > 50
                self.memory.add_memory(response, {"source": "loop"})
                self.data_moat.add_data(f"refined_{task}", {"response": response, "trace_id": trace["id"]})
                break  # Converge early

            task = f"Refine: {response}"  # Loop refinement

        return response