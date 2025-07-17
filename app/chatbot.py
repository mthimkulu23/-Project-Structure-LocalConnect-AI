from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv # Make sure this is imported if you're loading .env


# No need for this if we're not using LocationManager or search_local_services
# from app.services import LocationManager, search_local_services


class LocalConnectChatbot:
    def __init__(self):

        try:

            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"), # This is for Gemini
                temperature=0.7
            )
            print("Google Gemini client initialized.")
        except Exception as e:
            print(f"Error initializing Google Gemini client: {e}")
            self.llm = None

        # Remove or comment out this line:
        # self.location_manager = LocationManager()


        self.prompt_template = PromptTemplate(
            input_variables=["query", "location_info"],
            template=(
                "You are LocalConnect AI, an intelligent assistant specializing in local services. "
                "Your goal is to provide helpful information, especially regarding local businesses, "
                "services, and general knowledge, considering the user's location if provided. "
                "If the query is a general question, answer it directly.\n\n"
                "User's Current/Requested Location: {location_info}\n"
                "User Query: {query}\n\n"
                "Response:"
            )
        )


        if self.llm:
            self.llm_chain = LLMChain(prompt=self.prompt_template, llm=self.llm)
        else:
            self.llm_chain = None
            print("LLMChain not initialized due to LLM failure.")


    async def process_query(self, query: str, location: str = "current_location") -> str:
        location_info = ""
        # location_coords = None # No longer needed

        # Remove or comment out this entire block, as it handles geocoding
        # if location and location != "current_location":
        #     geocoded_data = await self.location_manager.geocode_location(location)
        #     if geocoded_data:
        #         location_info = f"Latitude: {geocoded_data['latitude']}, Longitude: {geocoded_data['longitude']}, " \
        #                         f"Address: {geocoded_data['address']}"
        #         location_coords = (geocoded_data['latitude'], geocoded_data['longitude'])
        #     else:
        #         print(f"Could not geocode location: {location}. Using original string for info.")
        #         location_info = location

        # For now, we'll just pass the original location string to the prompt
        if location and location != "current_location":
            location_info = location
        else:
            location_info = "Not provided or default" # Or "" if you prefer to omit


        if not self.llm_chain:
            return "I'm sorry, the AI service is not properly initialized. Please check backend logs."

        try:
        

            print("Proceeding with general LLM query.")
            response = await self.llm_chain.arun(query=query, location_info=location_info)
            return response
        except Exception as e:
            if "insufficient_quota" in str(e).lower() or "quota" in str(e).lower():
                error_message = "I'm sorry, the Google API quota has been exceeded or billing is not set up. Please check your Google Cloud Console."
            else:
                error_message = f"An error occurred while processing your query: {e}"
            print(f"Error during LLM or service call: {e}")
            return error_message