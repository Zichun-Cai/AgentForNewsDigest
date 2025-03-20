import os
from dotenv import load_dotenv
import autogen
import asyncio
from fetch_kol import fetch_kol_posts

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
# 1.0 配置Agent的LLM
llm_config = {
    "config_list": config_list_deepseek
}
# 1.1 KOLMonitorAgent
# 1.1 该Agent负责从API接口获取Twitter KOL发布的内容，并进行初步处理。
KOLMonitorAgent = autogen.AssistantAgent(
    name="KOLMonitor",
    llm_config=llm_config,
    system_message="你是一位专业的Web3交易分析师, 通过基于Twitter KOL发布的内容，分析市场趋势。"
)   

# 1.2 MarketDataAgent
# 1.2 该Agent负责获取分析实时市场数据(实时链上交易数据)，并进行初步处理。
MarketDataAgent = autogen.AssistantAgent(
    name="MarketDataAnalyst",
    llm_config=llm_config,
    system_message="你是一位专业的Web3交易分析师, 通过基于实时链上数据，分析市场趋势。"
)   

# 1.3 StrategyAgent 
# 1.3 该Agent负责综合KOLMonitorAgent和MarketDataAgent的分析结果，生成交易策略。
StrategyAgent = autogen.AssistantAgent(
    name="StrategyMaker",
    llm_config=llm_config,
    system_message="你是专业的Web3交易决策者，通过分析KOLMonitorAgent和MarketDataAgent的分析结果，生成交易策略。"
)

# 1.4 UserProxyAgent
# 1.4 该Agent负责协调各个Agent的工作流程
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    system_message="负责协调各个Agent的工作流程",
    human_input_mode="NEVER"
)

async def kol_pipeline():
    """KOL数据获取和分析的完整流程"""
    # 1. 获取KOL原始数据
    kol_raw_data = fetch_kol_posts(hours=24, limit=100)['data']
    if kol_raw_data:
        print("KOL原始数据获取成功")
    else:
        print("KOL原始数据获取失败")
        kol_raw_data = "KOL原始数据获取失败"
    
    # 2. KOL数据分析
    kol_analysis_response = user_proxy.initiate_chat(
        KOLMonitorAgent,
        message=f"""请依据最近24小时KOL发布的前100条内容，分析市场趋势。
        请提供详细的KOL数据分析。
        
        原始数据如下：
        {kol_raw_data}
        """,
        max_turns=1  # 限制对话轮次为1
    )
    
    return {
        "raw_data": kol_raw_data,
        "analysis": kol_analysis_response.chat_history[-1]['content']
    }

async def trading_pipeline():
    """交易决策流水线"""
    try:
        print("开始执行交易决策流水线...")
        
        # 1. 创建KOL任务
        kol_task = asyncio.create_task(kol_pipeline())
        
        # 2. 直接获取市场分析结果（不需要await）
        market_result = user_proxy.initiate_chat(
            MarketDataAgent,
            message="""请分析当前链上数据，重点关注：
            1. 交易量异常
            2. 大户活动
            3. DEX流动性变化
            4. Gas费用趋势""",
            max_turns=1
        )
        
        # 3. 等待KOL任务完成
        kol_result = await kol_task
        
        # 4. 从ChatResult对象中获取内容
        market_analysis = market_result.chat_history[-1]['content']
        
        # 5. 将两份分析结果发送给StrategyAgent
        strategy_prompt = f"""
        请基于以下三个数据源制定交易策略：
        
        1. KOL数据分析：
        {kol_result['analysis']}
        
        2. 链上数据分析：
        {market_analysis}
        
        3. 原始KOL数据：
        {kol_result['raw_data']}
        """
        
        strategy_response = user_proxy.initiate_chat(
            StrategyAgent,
            message=strategy_prompt,
            max_turns=1
        )
        
        return {
            "kol_raw_data": kol_result['raw_data'],
            "kol_analysis": kol_result['analysis'],
            "market_analysis": market_analysis,
            "strategy": strategy_response.chat_history[-1]['content']
        }
        
    except Exception as e:
        print(f"执行流水线时出错: {str(e)}")
        return {
            "error": str(e)
        }


async def main():
    """主函数 - 只运行一次完整流程"""
    try:
        print("\n=== 开始执行交易决策流程 ===")
        
        print("\n2. 执行交易决策流水线...")
        result = await trading_pipeline()
        
        # 输出结果
        print("\n=== 执行结果 ===")
        if "error" in result:
            print("执行出错:", result["error"])
            return
        print("========================================================================================================================================================================================================")
        print("KOL数据分析:", result["kol_analysis"])
        print("========================================================================================================================================================================================================")
        print("\n市场数据分析:", result["market_analysis"])
        print("========================================================================================================================================================================================================")
        print("\n交易策略:", result["strategy"])
        print("========================================================================================================================================================================================================")
        print("\n=== 流程执行完成 ===")
        
    except Exception as e:
        print(f"\n❌ 执行过程中出现错误: {str(e)}")
    finally:
        print("\n程序结束")


if __name__ == "__main__":
    print("开始执行交易决策流程...")
    asyncio.run(main())