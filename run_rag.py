
from app.graph import LLMNodeGraph
from app.embeddings import Embeddings
from langchain.schema.messages import AIMessageChunk

file_name = 'faiss_index'
embeddings = Embeddings(file_name)

memory = False
tools = False
streaming = False

llm_node_graph = LLMNodeGraph(memory=memory)
graph = llm_node_graph.chatbot_tools() if tools else llm_node_graph.chatbot()

# 查看langgraph执行节点流程图, 需要先执行"chatbot_tools()" or "chatbot()" 函数
# llm_node_graph.show_graph()


def stream_graph_updates(user_input: str, memory: bool = False, streaming: bool = False):

    config = {"configurable": {"thread_id": "5"}} if memory else {}
    stream_mode = 'messages' if streaming else 'values'

    results = embeddings.query(user_input)
    answer = ''

    for doc in results:
        answer += doc.page_content

    content = f"""
    已知信息:
    {answer}

    用户问题:
    {user_input}
    """

    for event in graph.stream(
        {"messages": [
            {"role": "user", "content": content}]
        },
        config,
        stream_mode=stream_mode      
        ):

        if streaming:
            if isinstance(event[0], AIMessageChunk):
                print(event[0].content, end="", flush=True)
        else: 
            if "messages" in event:
                event["messages"][-1].pretty_print()

while True:
    try:
        user_input = input("\nUser(quit、exit、q): ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input, memory=memory, streaming=streaming)
    except Exception as e:
        print(e)
        print("Exit goodbye!")
        break
