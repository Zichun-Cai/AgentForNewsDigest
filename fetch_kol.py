import requests
from typing import Optional, Dict

def fetch_kol_posts(
    hours: Optional[int] = 4,
    limit: Optional[int] = 100,
    timeout: int = 15
) -> Dict:
    """
    获取指定时间范围内的KOL推文
    
    :param hours: 查询时间范围（小时），默认4小时
    :param limit: 最大返回条目数，默认100条
    :param timeout: 请求超时时间（秒）
    :return: 包含推文数据的字典
    """
    # 基础URL
    base_url = "http://18.166.51.162:5555/czlfl7q8cb4cfukuy90ukt8/ai/api/twitter/getKolPosts"
    
    try:
        # 构造请求参数
        params = {
            "hours": max(1, hours),  # 确保最小值为1小时
            "limit": min(1000, limit) # 限制最大1000条防止API限制
        }
        
        # 发送GET请求
        response = requests.get(
            url=base_url,
            params=params,
            timeout=timeout
        )
        
        # 检查HTTP状态码
        response.raise_for_status()
        
        # 返回JSON响应
        return response.json()
    
    except requests.RequestException as e:
        print(f"API请求失败: {str(e)}")
        return {"error": str(e)}
    except ValueError:
        print("响应解析失败")
        return {"error": "Invalid JSON response"}

# 使用示例
if __name__ == "__main__":
    # 使用默认参数
    print(fetch_kol_posts())  # hours=4, limit=100
    
    # 自定义参数
    print(fetch_kol_posts(hours=24, limit=500))
    
    # 处理异常参数
    print(fetch_kol_posts(hours=-5, limit=1500))  # 自动修正为hours=1, limit=1000