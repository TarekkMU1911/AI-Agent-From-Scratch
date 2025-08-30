from pydantic import BaseModel

class ResearchResponse (BaseModel) :
    topic : str
    summary  : str
    sources : list[str]
    usedTools : list[str]
    