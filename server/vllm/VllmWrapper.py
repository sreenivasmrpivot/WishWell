# from vllm import LLM, SamplingParams

# from models import Wish

# class VllmWrapper:
    
#     def __init__(self, wish: Wish):
#         self.wish = wish

#     def _load_params(self):
#         self.sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

#     def _load_llm(self):
#         self.llm = LLM(model=self.wish.modelName)

#     def run(self):
#         output = self.llm.generate([self.wish.whisper], self.sampling_params)
#         grant = output.outputs[0].text
#         return grant