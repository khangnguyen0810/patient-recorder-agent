import yaml
import os

def extract_instruction(filename: str) -> str:
    instruction = ""
    try:
        agent_dir = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(agent_dir, filename)
        
        file_extension = os.path.splitext(filename)[1].lower()
        
        with open(filepath, "r", encoding="utf-8") as f:
            if file_extension == '.yaml' or file_extension == '.yml':
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    instruction = (
                        data.get('content') or 
                        data.get('instruction') or 
                        data.get('prompt') or
                        data.get('text') or
                        str(data)
                    )
                else:
                    instruction = str(data)
            else:
                instruction = f.read()
        
        print(f"Successfully loaded instruction from {filename}")
    except FileNotFoundError:
        print(f"WARNING: Instruction file not found: {filepath}.")
    except yaml.YAMLError as e:
        print(f"ERROR parsing YAML file {filepath}: {e}.")
    except Exception as e:
        print(f"ERROR loading instruction file {filepath}: {e}.")
    return instruction