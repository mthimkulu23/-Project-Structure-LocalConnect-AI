# LocalConnectAI/app/chatbot.py

# Import necessary components
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os 
from app.services import LocationManager, search_local_services


class LocalConnectChatbot:
    def __init__(self):
       
        try:
           
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", # Changed to a currently supported model
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7
            )
            print("Google Gemini client initialized.")
        except Exception as e:
            print(f"Error initializing Google Gemini client: {e}")
            self.llm = None 

        # Initialize LocationManager
        self.location_manager = LocationManager()

        # Define the prompt template for the chatbot
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

        # Initialize the LangChain LLMChain
        if self.llm:
            self.llm_chain = LLMChain(prompt=self.prompt_template, llm=self.llm)
        else:
            self.llm_chain = None
            print("LLMChain not initialized due to LLM failure.")

   


    async def process_query(self, query: str, location: str = "current_location") -> str:
        location_info = ""
        location_coords = None

        if location and location != "current_location":
            geocoded_data = await self.location_manager.geocode_location(location)
            if geocoded_data:
                location_info = f"Latitude: {geocoded_data['latitude']}, Longitude: {geocoded_data['longitude']}, " \
                                f"Address: {geocoded_data['address']}"
                location_coords = (geocoded_data['latitude'], geocoded_data['longitude']) # Store coords
            else:
                print(f"Could not geocode location: {location}. Using original string for info.")
                location_info = location # Fallback to original string if geocoding fails

        # If LLM failed to initialize, return an error message
        if not self.llm_chain:
            return "I'm sorry, the AI service is not properly initialized. Please check backend logs."

        try:
          
            service_types = ["police station", "dentist", "restaurant", "event"]
            found_service_type = None
            for s_type in service_types:
                if s_type in query.lower():
                    found_service_type = s_type
                    break

            if found_service_type:
                # If a service type is detected, call the search_local_services
                print(f"Detected service search for: {found_service_type}")
                
                service_results = await search_local_services(
                    service_type=found_service_type,
                    location_coords=location_coords,
                    location_name=location 
                )
                if service_results:
                    formatted_results = "\n".join([f"- {s.get('name')}, Address: {s.get('address')}, Rating: {s.get('rating', 'N/A')}" for s in service_results])
                    return f"Here are some {found_service_type}s I found:\n{formatted_results}"
                else:
                    return f"I couldn't find any {found_service_type}s in that area using Google Places or mock data."
        
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