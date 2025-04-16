from langgraph.graph import StateGraph, START, END
from app.llm import LLM
from langgraph.graph.message import add_messages
from typing import Annotated, List
from typing_extensions import TypedDict
from app.tools import TOOLS
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import RemoveMessage
from langchain.schema.messages import SystemMessage, HumanMessage

from PIL import Image
import io

llm = LLM()

class State(TypedDict):
    messages: Annotated[list, add_messages]


class LLMNodeGraph():

    def __init__(self, memory: bool = False, k: int = 3):
        print('Graph => START')

        self.chat = None

        self.graph_builder = StateGraph(State)
        self.graph = None

        self.memory = memory
        self.k = k
        pass
    

    def _invoke(self, state: State):

        message = self.chat.invoke(state["messages"])
   
        assert len(message.tool_calls) <= 1
        return {"messages": [message]}
    
    async def _ainvoke(self, state: State):

        message = await self.chat.ainvoke(state["messages"])
   
        assert len(message.tool_calls) <= 1
        return {"messages": [message]}
    
    def _filter_messages(self, state: State):

        messages = state['messages']
        humna_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
        remove_system_messages = []
        remove_chat_messages = []

        if (isinstance(messages[0], SystemMessage)):
            system_messages = [msg for msg in messages if isinstance(msg, SystemMessage)]
            remove_system_messages = [RemoveMessage(m.id) for m in (system_messages[1:])]

            messages =  [msg for msg in state['messages'] if not isinstance(msg, SystemMessage)]
   
        if (len(humna_messages) >= self.k + 1):
            i = len(messages) - messages.index(humna_messages[-self.k])
            remove_chat_messages = [RemoveMessage(m.id) for m in messages[:-i]]


        if (remove_system_messages or remove_chat_messages):
            return { "messages": remove_chat_messages + remove_system_messages }
            
    def _compile(self):

        if self.memory:
            memory = MemorySaver()
            self.graph = self.graph_builder.compile(checkpointer=memory)
        else:
            self.graph = self.graph_builder.compile()
        return self.graph


    def chatbot(self, async_invoke: bool = False):

        self.chat = llm.ask()

        self.graph_builder.add_node("chatbot", self._ainvoke if async_invoke else self._invoke)

        if (self.memory):
            self.graph_builder.add_node('filter_messages', self._filter_messages)

            self.graph_builder.add_edge(START, "filter_messages")
            self.graph_builder.add_edge('filter_messages', "chatbot")
        else:
            self.graph_builder.add_edge(START, "chatbot")

        self.graph_builder.add_edge('chatbot', END)

        return self._compile()
    

    def chatbot_tools(self, tools: List = TOOLS, async_invoke: bool = False):

        self.chat = llm.ask_tools(tools)

        self.graph_builder.add_node("chatbot", self._ainvoke if async_invoke else self._invoke)
        self.graph_builder.add_node("tools", ToolNode(tools=tools))

        if (self.memory):
            self.graph_builder.add_node('filter_messages', self._filter_messages)

            self.graph_builder.add_edge(START, "filter_messages")
            self.graph_builder.add_edge('filter_messages', "chatbot")
        else:
            self.graph_builder.add_edge(START, "chatbot")

        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_conditional_edges('chatbot', tools_condition, { "tools": "tools", END: END })

        return self._compile()
    
    def show_graph(self):
        print('show_graph => START')
        if self.graph:
            png_data = self.graph.get_graph().draw_mermaid_png()
            img = Image.open(io.BytesIO(png_data))
            img.show()
            print('show_graph => SUCCESS')
        else:
            print('show_graph => Execute the "chatbot function" or "chatbot_tools function" first')
