from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool 
from datetime import datetime
from save import save2text
import os
import json

with open(os.path.join(os.path.dirname(__file__), "messages.json"), "r", encoding="utf-8") as f:
    messages = json.load(f)

# Search tool
search = DuckDuckGoSearchRun()
DESCRIPTION = messages.get("DESCRIPTION")
searchTool = Tool(name="search", func=search.run, description=DESCRIPTION)

# Wikipedia tool
apiWrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=10000)
wikiTool = WikipediaQueryRun(api_wrapper=apiWrapper)

# Save tool
SAVE_DESCRIPTION = messages.get("SAVE_DESCRIPTION")
saveTool = Tool(name="save_text_to_file", func=save2text, description=SAVE_DESCRIPTION)
