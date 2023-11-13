from models import DeviceEnum, Wish
from channel.langchain.LangChainWrapper import LangChainWrapper
from channel.llamaindex.LlamaIndexWrapper import LlamaIndexWrapper
# from channel.vllm.VllmWrapper import VllmWrapper
from channel.vmwarevllmapi.VmwareVllmApiWrapper import VmwareVllmApiWrapper

def process_wish(wish: Wish):
    if wish.channel == "Langchain":
        langChainWrapper = LangChainWrapper(wish)
        grant = langChainWrapper.run()
        return grant
    elif wish.channel == "Llamaindex":
        llamaIndexWrapper = LlamaIndexWrapper(wish)
        grant = llamaIndexWrapper.run()
        return grant
    # elif wish.channel == "Vllm":
        # if wish.device == DeviceEnum.CPU:
            # raise Exception("Vllm does not work on CPU, it requires CUDA")
        # 
        # vllmWrapper = VllmWrapper(wish)
        # grant = vllmWrapper.run()
        # return grant
    elif wish.channel == "VmwareVllmApi":
        vmwareVllmApiWrapper = VmwareVllmApiWrapper(wish)
        grant = vmwareVllmApiWrapper.run()
        return grant
    else:
        raise Exception("Channel not supported")
        
if __name__ == '__main__':
    wish = Wish(location="local", documentName="Business Conduct.pdf", modelName="Llama", channel="Llamaindex", whisper="what is Legal Holds?")
    process_wish(wish)