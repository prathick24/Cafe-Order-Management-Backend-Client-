import boto3
from langchain_aws import ChatBedrock
import os
from dotenv import load_dotenv

load_dotenv()

class Config:


    def get_bedrock_client():
        """Create and return a Bedrock runtime client."""
        return boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("REGION")
        )


    def get_llm(self , max_tokens=500, temperature=0.7):
        """Create and return a ChatBedrock LLM instance."""
        return ChatBedrock(
            client=Config.get_bedrock_client(),
            model_id=os.getenv("MODEL_ID"),
            provider="amazon",
            model_kwargs={
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
