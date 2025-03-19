import os
from dotenv import load_dotenv
import pyautogen as autogen

# 0 加载环境变量
load_dotenv()

# 0.1 API信息获取
TWITTER_API_BASE_URL = os.getenv("TWITTER_API_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
TARGET_TWITTER_USERNAME = os.getenv("TARGET_TWITTER_USERNAME")

# 0.2 LLM API配置信息
# 0.2.1 OpenAI API
config_list_openai = [
    {
        "model": "gpt-4o",
        "api_key": OPENAI_API_KEY,
    }
]
# 0.2.2 DeepSeek API
config_list_deepseek = [
    {
        "model": "deepseek-chat",
        "api_key": DEEPSEEK_API_KEY,
        "base_url": "https://api.deepseek.com/v1",
    }
]

# 1 创建服务Agent，包含KOLMonitorAgent、MarketDataAgent、StrategyAgent、CodeGenAgent、ExecutorAgent
# 1.1 KOLMonitorAgent
# 1.1 该Agent负责从API接口获取Twitter KOL发布的内容，并进行初步处理。
KOLMonitorAgent = autogen.AssistantAgent(
    name="KOL Monitor",
    llm_config=False,
    system_message="你负责收集Twitter KOL发布的内容，并进行初步处理，分析推特侧市场讯息。"
)   


# 1.2 MarketDataAgent
# 1.2 该Agent负责获取分析实时市场数据(实时链上交易数据)，并进行初步处理。
MarketDataAgent = autogen.AssistantAgent(
    name="Market Data Analyst",
    llm_config=config_list_openai,
    system_message="你是一位专业的Web3交易分析师, 通过基于实时链上数据，分析市场趋势。"
)   

# 1.3 StrategyAgent 
# 1.3 该Agent负责综合KOLMonitorAgent和MarketDataAgent的分析结果，生成交易策略。
StrategyAgent = autogen.AssistantAgent(
    name="Strategy Maker",
    llm_config=config_list_openai,
    system_message="你是专业的Web3交易决策者，通过分析KOLMonitorAgent和MarketDataAgent的分析结果，生成交易策略。"
)

# 1.4. CodeGenAgent
# 1.4 该Agent负责将交易策略转化为代码。
CodeGenAgent = autogen.AssistantAgent(
    name="Code Generator",
    llm_config=config_list_openai,
    system_message="你是一个交易策略的代码生成器，基于交易机器人指令的语法，根据交易策略，生成交易机器人指令。"
)

# 1.5 ExecutorAgent
# 1.5 该Agent负责将交易指令发送给到指定推特账户，由推特账户背后的交易机器人执行交易
ExecutorAgent = autogen.AssistantAgent(
    name="Trading Bot Executor",
    llm_config=config_list_openai,
    system_message="你负责将交易指令发送给到指定推特账户，使推特账户背后的交易机器人执行交易。"
)







