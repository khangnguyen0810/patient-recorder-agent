def extract_instruction(data) -> str:
    if isinstance(data, dict):
        return (
            data.get('content') or
            data.get('instruction') or
            data.get('prompt') or
            data.get('text') or
            str(data)
        )
    return str(data)