
<h1 style="text-align: center;"></h1>

# LangGraph Start

这是一个简单的langGraph示例，快速入门即上手😊 

<br>
已使用的文档如下：

1、[Langchain LLM](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html#chatopenai)
、[LLM key](https://bailian.console.aliyun.com/?tab=model#/model-market)

2、[Langgraph Quickstart](https://langchain-ai.github.io/langgraph/tutorials/introduction/)

3、[How to create and query vector stores](https://python.langchain.com/docs/how_to/vectorstores/) => 使用的为```OpenAIEmbeddings```需要付费，替换为[HuggingFaceEmbeddings](https://python.langchain.com/api_reference/huggingface/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html#langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings)即可

<br>
已实现功能如下：

1、Chatbot

2、Function calling

3、RAG


## 安装指南

确保已有Python环境，当前使用```Python v3.13.2```

1、克隆仓库
```bash
git clone https://github.com/angxuejian/langgraph-start.git
```

2、安装依赖
```
pip install -r requirements.txt
```

## 配置说明
需要配置LLM、Web，步骤如下

1、在```config```目录下创建```config.py```文件 (可从```config.example.py```文件复制)

2、添加API密钥，可申请[百炼LLM](https://bailian.console.aliyun.com/?tab=model#/model-market)、[Tavily Web](https://app.tavily.com/home)，均有免费Token使用
```py

# Global LLM configuration
# 阿里云百炼 https://bailian.console.aliyun.com/?tab=model#/model-market
llm = {
    "openai_api_key": 'YOUR_API_KEY',
    "openai_api_base": 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    "model_name": 'qwen-max' # 根据千问文档选择合适的模型，例如 qwen-turbo 或 qwen-plus
}


# Global Web configuration
# tavily https://app.tavily.com/home
web = {
    "tavily_api_key": "YOUR_API_KEY"
}
```
## 运行说明

> 需要科学上网，才能运行；以下命令都在```langgraph-start```目录下执行

1、运行chatbot，根据配置可使用```tools```、```memory```功能
```bash
python main.py
```

2、运行chatbot rag

默认读取```faiss_index```文件，可修改```file_name```来选择读取文件; ```faiss_index```源文件为```basedata.txt```

```bash
python run_rag.py
```

3、自定义文本内容，将其向量化

- ```file_name```：向量化后的文件名称
- ```source_file_name```：源文件名称

```bash
python run_vector.py
```

> 本地会加载```BAAI/bge-base-zh```模型，推理速度因电脑差异会有快慢之分，没看到控制台输出```HuggingFaceEmbeddings done !```前，均还在推理，切勿退出。只有运行```run_rag.py```和```run_vector.py```才会使用到向量化

4、mcp server，在cursor、windsurf、claude等应用上，打开```mcp.json```，将以下配置复制粘贴
```json
// windows
{
  "mcpServers": {
    "tools-server": {
      "command": "python",
      "args": [
        "C:\\ABSOLUTE-PATH\\XXXXXXX\\langgraph-start\\mcp\\server.py" 
      ]
    }
  }
}

// MacOS or Linux
{
  "mcpServers": {
    "tools-server": {
      "command": "python",
      "args": [
        "/ABSOLUTE-PATH/XXXXXXX/langgraph-start/mcp/server.py" 
      ]
    }
  }
}
```

目前只有```get_current_time_mcpfunction```一个函数，询问当前时间，即可调用。

5、mcp client，执行本地Mcp server工具
```bash
python .\mcp\client.py .\mcp\server.py
```
> 可替换成其他mcp工具，修改```client.py```文件中的```StdioServerParameters(command='', args=[], env=None)```参数即可


## 交流

可通过 ✉️ 邮箱联系@angxuejian: xuejian.ang@gmail.com

or [Issues](https://github.com/angxuejian/langgraph-start/issues)

希望 LangGraph Start 可以帮助你快速了解 + 上手AI应用😎


<!-- packages

pip install langchain
pip install langchain-openai
pip install langchain-community
pip install langchain-huggingface
pip install faiss-cpu
pip install Pillow
pip install langgraph

-->
