import json
import openai
from helper import get_model_path

from models import Wish

class VmwareVllmApiWrapper:
    
    cred_file = "./creds.json"
    endpoint = "https://vllm.libra.decc.vmware.com/api/v1"
    prompt = """Act as a team member greeter.

    ---

    Follow the following format:

    ### Instruction: ${a request for greeting}
    ### Response: ${a friendly and polite greeting}

    ---

    ### Instruction: Say hello to Sreenivas
    ### Response:"""

    def __init__(self, wish: Wish):
        self.wish = wish
        
    def _load_creds(self):
        with open(VmwareVllmApiWrapper.cred_file, "r") as creds:
            api_key = json.loads(creds.read())["api_key"]
            self.api_key = api_key
    
    def _initialize_openai_settings(self):
        self.openai.api_key = self.api_key
        self.openai.api_base = VmwareVllmApiWrapper.endpoint
    
    def run(self):
        grant = openai.Completion.create(
            model=get_model_path(self.wish),
            prompt=VmwareVllmApiWrapper.prompt,
            max_tokens=1024,
            temprature=0,
            stream=False
        )        
        return grant