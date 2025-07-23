from langchain.chains import LLMChain
from langchain_groq import ChatGroq 
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv # Make sure this is imported if you're loading .env


class LocalConnectChatbot:
    def __init__(self):
        
        load_dotenv() 

        try:
            self.llm = ChatGroq(
               
                model="llama3-8b-8192", 
                temperature=0.7
            )
            print("Groq LLM client initialized.")
        except Exception as e:
            print(f"Error initializing Groq LLM client: {e}")
            self.llm = None

        # self.location_manager = LocationManager() # Keep this commented out as before

        self.prompt_template = PromptTemplate(
            input_variables=["query", "location_info"],
            template=(
                "You are LocalConnect AI, an intelligent assistant specializing in local services. "
                "Your goal is to provide helpful information, especially regarding local businesses, "
                "services, and general knowledge, considering the user's location if provided. "
                "If the query is a general question, answer it directly.\n\n"
                # --- START: Added specific instruction for creator identity ---
                "If the user asks who built you, created you, or developed you, "
                "your response MUST be: 'I was built by Thabang Mthimkulu.' Do NOT provide any other information.\n\n"
                # --- END: Added specific instruction for creator identity ---
                "User's Current/Requested Location: {location_info}\n"
                "User Query: {query}\n\n"
                "Response:"
            )
        )

        # Removed the DeprecationWarning fix for LangChain, assuming you want to keep the current structure for now
        # You might see a new warning from LangChain about LLMChain, but it should still work.
        if self.llm:
            self.llm_chain = LLMChain(prompt=self.prompt_template, llm=self.llm)
        else:
            self.llm_chain = None
            print("LLMChain not initialized due to LLM failure.")

    async def process_query(self, query: str, location: str = "current_location") -> str:
        location_info = ""

        if location and location != "current_location":
            location_info = location
        else:
            location_info = "Not provided or default" # Or "" if you prefer to omit

        if not self.llm_chain:
            return "I'm sorry, the AI service is not properly initialized. Please check backend logs."

        try:
            print("Proceeding with LLM query via Groq.")
            response = await self.llm_chain.arun(query=query, location_info=location_info)
            # --- ADD THIS LINE FOR DEBUGGING ---
            print(f"DEBUG: LLMChain raw response type: {type(response)}, value: '{response}'")
            # --- END DEBUGGING LINE ---
            return response
        except Exception as e:
            # Modify error handling to be more generic, as 'quota' specific to Google might not apply to Groq
            # Though Groq does have rate limits, the error message might be different.
            error_message = f"An error occurred while processing your query with Groq: {e}"
            print(f"Error during LLM or service call: {e}")
            return error_message