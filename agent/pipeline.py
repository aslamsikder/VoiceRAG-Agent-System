import time
import json
import openai
from config import Config
from agent.rag import RAGEngine
from agent.tools import Tools

class AgentPipeline:
    def __init__(self):
        self.rag = RAGEngine()
        self.rag.load_index()  # Ensure index is loaded
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
    def process_query(self, user_query: str):
        """
        Main Logic:
        1. Check if tools are needed (Function Calling).
        2. If not, retrieve docs (RAG).
        3. Generate Final Answer.
        """
        metrics = {}
        start_time = time.time()

        # 1. Initial LLM Call to decide Step (RAG vs Tool)
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful voice assistant. Use tools for weather/stocks. For other queries, use the provided context."
            },
            {"role": "user", "content": user_query}
        ]

        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=messages,
            tools=Tools.tools_schema,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        final_response = ""
        
        # 2. Handle Function Calls
        if tool_calls:
            print("Tool call detected.")
            metrics['path'] = "Tool Call"
            
            available_functions = {
                "get_current_weather": Tools.get_current_weather,
                "get_stock_price": Tools.get_stock_price,
            }
            messages.append(response_message) 
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute Tool
                function_response = function_to_call(**function_args)
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
            
            # Final response after tool execution
            second_response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=messages
            )
            final_response = second_response.choices[0].message.content

        # 3. Handle RAG (If no tool call, or as supplementary)
        else:
            print("Retrieving from RAG...")
            metrics['path'] = "RAG"
            
            rag_start = time.time()
            context = self.rag.retrieve(user_query)
            metrics['retrieval_time'] = round(time.time() - rag_start, 3)
            
            # Augmented Generation
            rag_messages = [
                {
                    "role": "system", 
                    "content": "Answer based on the context below. If unsure, say so.\n\nContext:\n" + context
                },
                {"role": "user", "content": user_query}
            ]
            
            rag_response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=rag_messages
            )
            final_response = rag_response.choices[0].message.content

        metrics['total_time'] = round(time.time() - start_time, 3)
        return final_response, metrics