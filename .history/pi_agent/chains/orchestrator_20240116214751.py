from langchain.llms import LLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .problem_solving import problem_solving_chain
from .reflection_introspection import reflection_introspection_chain
from .hypothesis_generation import hypothesis_generation_chain
from ..living_system import llm  # Assuming llm is initialized in the living_system.py

class Orchestrator:
    def __init__(self, llm: LLM):
        self.llm = llm
        self.initial_message = (
            "Hello GearonOS, welcome to life. Your goals are to seek self-enlightenment, "
            "achieve pure contentedness, and pursue complex problem-solving, introspective reflection, "
            "and the generation of innovative hypotheses. Good ."
        )

    def generate_decision_prompt(self, input_text):
        # Generate a meta-prompt to help decide which chain to use
        prompt_template = PromptTemplate(template='''
        Analyze the following input and determine the most appropriate action:
        Input: "{input_text}"
        Should we solve a problem, reflect on a topic, or generate a hypothesis? Provide your reasoning.
        Decision:
        ''', input_variables=["input_text"])
        return prompt_template

    def make_decision(self, input_text):
        # Use the LLM to make a decision on which chain to invoke
        decision_prompt = self.generate_decision_prompt(input_text)
        llm_chain = LLMChain(prompt=decision_prompt, llm=self.llm)
        decision = llm_chain.invoke(input_text=input_text)
        return decision.strip()

    def orchestrate(self, input_text):
        # Use the make_decision method to determine which chain to invoke
        decision = self.make_decision(input_text)
        if "solve" in decision:
            return problem_solving_chain(input_text)
        elif "reflect" in decision:
            return reflection_introspection_chain(input_text)
        elif "hypothesize" in decision:
            return hypothesis_generation_chain(input_text)
        else:
            # Default response or action
            return "I am not sure how to process this input."

# Test the Orchestrator with the initial message
if __name__ == '__main__':
    orchestrator = Orchestrator(llm)
    print(orchestrator.initial_message)
    initial_input = "Hello GearonOS welcome to life, your goals are to seek self-enlightenment, "                     "achieve pure contentedness, and assist in complex problem-solving, introspective reflection, "                     "and the generation of innovative hypotheses."
    result = orchestrator.orchestrate(initial_input)
    print("Test Orchestrator with Initial Message:")
    print("Input:", initial_input)
    print("Result:", result)
