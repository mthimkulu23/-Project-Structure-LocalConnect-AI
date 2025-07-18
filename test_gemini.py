

import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env file.")
else:
    print("Gemini API Key loaded successfully.")
    try:
        genai.configure(api_key=GEMINI_API_KEY)

        print("\n--- Listing available Gemini models ---")
        found_gemini_pro = False
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"  Model: {m.name}, Supported methods: {m.supported_generation_methods}")
                if m.name == "models/gemini-1.0-pro":
                    found_gemini_pro = True

        if not found_gemini_pro:
            print("\nWARNING: 'models/gemini-1.0-pro' was NOT found in the list of supported models for your API key.")
            print("This indicates a problem with your Google Cloud Project / API Key setup for this model.")
            print("Please ensure 'Generative Language API' is enabled and you have the correct key for a project that supports this model.")
            print("You might need to try a different region or re-check your Google Cloud Console settings.")
        else:
            print("\nSUCCESS: 'models/gemini-1.0-pro' found and supports generateContent!")


        print("\n--- Testing a simple 'generateContent' call with gemini-1.0-pro ---")
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content("What is the capital of France?")
        print("\nGemini Response:")
        print(response.text)
        print("\n--- Test Complete ---")

    except genai.types.BlockedPromptException as e:
        print(f"\nError: Prompt was blocked by safety settings: {e}")
    except Exception as e:
        print(f"\nAn error occurred during Gemini API call: {e}")
        print("This could be due to an invalid API key, API not enabled, or regional restrictions.")