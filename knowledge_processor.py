from ast import In
import os

from regex import P
from channel.langchain.knowledge_processor import KnowledgeProcessor as LCKnowledgeProcessor
from channel.llamaindex.knowledge_processor import KnowledgeProcessor as LIKnowledgeProcessor
import time
import argparse

from common.config import setup_logging_from_args, setup_logging_from_file
from common.logging_decorator import log_entry_exit, SensitiveData
from models import Information

@log_entry_exit()
def acquire_knowledge(information: Information):
    if information.integrator == "Langchain":
        langChainWrapper = LCKnowledgeProcessor(information)
        grant = langChainWrapper.learn()
        return grant
    elif information.integrator == "Llamaindex":
        llamaIndexWrapper = LIKnowledgeProcessor(information)
        grant = llamaIndexWrapper.learn()
        return grant
    else:
        raise Exception("Channel not supported")

@log_entry_exit()
def create_directory_structure():
    # Get the directory of the current script
    root_path = os.path.dirname(os.path.abspath(__file__))

    # Define the relative path for the new directory structure
    # new_dir_path = os.path.join(script_dir, "vector-store/langchain/faiss")

    # Create the directory structure if it doesn't exist
    # os.makedirs(new_dir_path, exist_ok=True)

    return root_path

def main(args):
    """The main function."""
    if args.config_file:
        setup_logging_from_file(args.config_file)
    else:
        setup_logging_from_args(args.log_level)

    # Start time
    start_time = time.time()
    information = Information(
        rootPath=create_directory_structure(), 
        folderName=args.folderName,
        documentName=args.documentName, 
        modelName=args.modelName, 
        device=args.device, 
        integrator=args.integrator, 
        vectorDatabase=args.vectorDatabase ,
        knowledgeBaseId=args.knowledgeBaseId
    )
    grant = acquire_knowledge(information)
    print(grant)
    # End time
    end_time = time.time()

    # Total time taken
    totalTimeTaken = (end_time - start_time) * 1000
    print()
    print(f"Runtime of the program is {totalTimeTaken}")
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--log_level", type=str, default="INFO", 
        help="Set the logging level (e.g., DEBUG, INFO, WARNING)"
    )

    parser.add_argument(
        "--config_file", type=str, default=None,
        help="Path to an alternate configuration file"
    )

    parser.add_argument(
        "--folderName", type=str, default="data", 
        help="Folder to get documents from."
    )

    parser.add_argument(
        "--documentName", type=str, default="Business Conduct.pdf", 
        help="Name of the document."
    )

    parser.add_argument(
        "--modelName", type=str, default="Llama", 
        help="Name of the model."
    )

    parser.add_argument(
        "--device", type=str, default="cpu", 
        help="Device to run the model on."
    )

    parser.add_argument(
        "--integrator", type=str, default="Langchain", 
        help="Name of the integrator."
    )

    parser.add_argument(
        "--vectorDatabase", type=str, default="faiss", 
        help="Name of the vector database."
    )

    parser.add_argument(
        "--knowledgeBaseId", type=str, default="123", 
        help="Id of the knowledge base."
    )
    
    args = parser.parse_args()
    main(args)    
