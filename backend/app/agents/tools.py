from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from app.core.config import settings
import requests
with open(settings.github_app_private_key_path, "r") as f:
    private_key = f.read()

search_tool = DuckDuckGoSearchRun()

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA','SSNLF') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=FOCXRSDUM6QXQQZ5"
    r = requests.get(url)
    print("tool called",url)
    return r.json() 

github = GitHubAPIWrapper(
    github_app_id=settings.github_app_id,
    github_app_private_key=private_key,
    github_repository=settings.github_repository,
)
github_toolkit = GitHubToolkit.from_github_api_wrapper(github)
github_tools = github_toolkit.get_tools()

import re

def sanitize_tool_name(name: str) -> str:
    name = name.lower()

    # Replace ANYTHING not allowed with underscore
    name = re.sub(r"[^a-z0-9_.:-]", "_", name)

    # Must start with letter or underscore
    if not re.match(r"^[a-z_]", name):
        name = f"tool_{name}"

    # Trim to 64 chars max
    return name[:64]


for tool in github_tools:
    tool.name = sanitize_tool_name(tool.name)

github_tools = [
    t for t in github_tools
    if t.name in ["read_file", "create_file", "update_file","create_pull_request","set_active_branch","create_a_new_branch"]
]
tools = [search_tool,calculator,get_stock_price,*github_tools]
