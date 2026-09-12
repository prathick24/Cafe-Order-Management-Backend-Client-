import boto3
from langchain_aws import ChatBedrock
from settings import config



class Config:


    def get_bedrock_client():
        """Create and return a Bedrock runtime client."""
        print("client created................")
        return boto3.client(
            service_name="bedrock-runtime",
            region_name=config.region
        )


    def get_llm(self , max_tokens = 500, temperature=0.7):
        """Create and return a ChatBedrock LLM instance."""
        return ChatBedrock(
            client=Config.get_bedrock_client(),
            model_id=config.model_id,
            provider=config.provider,
            model_kwargs={
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
