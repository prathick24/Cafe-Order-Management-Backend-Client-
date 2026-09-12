
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils.config import Config
from settings import config
from urllib.parse import quote_plus
from utils.exceptions.custom_app_exception import CustomAppException
from utils.exceptions.error_codes import ErrorCode , ErrorCodeStatus
from utils.exceptions.http_status import HttpStatusCode
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.resources import load_mcp_resources
from langchain_mcp_adapters.prompts import load_mcp_prompt
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain.agents.middleware import SummarizationMiddleware , HumanInTheLoopMiddleware
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command


class OrderAgent:
    def __init__(self):
        self.configure = Config()

    
    async def create_mcp_agent(self ,customer_id , question : str):

        
        PROMPT_ARGS = {
        "system_prompt": {"description": "system prompt assigned for the agent to follow"},
        "dish_making": {"description" : "Explain the process of making the dish"}
        }
        encoded_password = quote_plus(config.db_password)
        print("password created...........................")

        DB_URI = f"postgresql://{config.db_username}:{encoded_password}@{config.db_host}:{config.db_port}/{config.db_name}"
        print("URI created...........................")
        try:
            llm = Config.get_llm(self ,max_tokens=500, temperature=0.5)
            print("got llm..............")
            client = MultiServerMCPClient(
            {
                "my-server": {
                    "transport": "streamable_http",
                    "url": config.mcp_url,
                }
            }
         )   
           
            async with client.session("my-server") as session:

                tools = await load_mcp_tools(session)
                
                print("tools created...........................")
                
                blobs = await load_mcp_resources(session)
                

                resource_context = ""
                for blob in blobs:
                    try:
                        text = blob.as_bytes().decode("utf-8", errors="replace")
                        uri = blob.metadata.get("uri", "resource")
                        resource_context += f"\n[{uri}]\n{text}\n"
                    except Exception as e:
                        continue

                
                list_result = await session.list_prompts()
                
                available_prompts = list_result.prompts
                

                all_prompt_messages = []
                for prompt in available_prompts:
                    args     = PROMPT_ARGS.get(prompt.name, {})
                    
                    messages = await load_mcp_prompt(session, prompt.name, arguments=args)
                    
                    all_prompt_messages.extend(messages)
                    

                messages = list(all_prompt_messages)

                if resource_context:
                    messages.append(
                        HumanMessage(content=f"Available resources:\n{resource_context}")
                    )
                # print(messages)
                    
                print("context created...........................")
                async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
   
                    await checkpointer.setup()
                    print("tables created...........................")
                    
                    summarizer = SummarizationMiddleware(
                                model=Config.get_llm(self ,max_tokens=150, temperature=0), 
                                trigger=("tokens", 300),      
                                keep=("messages", 4),          
                                summary_prompt="""
                                        Summarize the conversation clearly and concisely.
                                        IMPORTANT: Always preserve:
                                        - User name
                                        - order items made by user
                                        - Users Favourite dish
                                    """
                                )
                    
                    print("Summarize created........")
                    confirm_order = HumanInTheLoopMiddleware(
                        interrupt_on={"place_order" : True}
                    )
                    print("HITL created")
                    
                    agent = create_agent(
                            model=llm,
                            tools=tools,
                            system_prompt=str(messages),
                            middleware=[summarizer , confirm_order],
                            checkpointer=checkpointer,  
                            )
                    
                    print("Agent created...........................")
                    runconfig = RunnableConfig(configurable={"thread_id": customer_id})
                    print("runcofig created...........................")

                    result = await agent.ainvoke(
                            {"messages": [{"role": "user" , "content": f"User with id {customer_id} asked {question}"}]}, runconfig
                            )
                    
                    if "__interrupt__" in result:
                        print("HUMAN APPROVAL REQUIRED!")


                        while True:
                            user_input = input("\nApprove? (yes/no): ").strip().lower()
                            if user_input in ["yes", "no"]:
                                break
                            print("❗ Please type 'yes' or 'no'")

                        decision = "approve" if user_input == "yes" else "reject"

                        final_result = await agent.ainvoke(
                            Command(resume={"decisions": [{"type": decision}]}),
                            config=runconfig,
                        )
                        return final_result["messages"][-1].content

                    else:
                        print("\n No interrupt triggered (tool not called)")
                        final = result["messages"][-1].content
                        return final
            
        except CustomAppException:
            raise
        except Exception as e:
            
            raise CustomAppException(
                message=f"Error in create llm or ivoke agent: {str(e)}",
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=HttpStatusCode.SERVICE_UNAVAILABLE,
                error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
            )

        

        