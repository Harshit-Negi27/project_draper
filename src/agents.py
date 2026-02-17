from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# RESEARCH AGENT
def research_logic(state):
    query = f"Analyze this product: {state['product_name']}. "
    if state['product_url']:
        query += f"URL: {state['product_url']}. "
    if state['product_description']:
        query += f"Context: {state['product_description']}."
        
    query += "Find unique selling points, target audience pains, and competitors."
    
    # Tavily Search
    print(f"DEBUG: Researching {state['product_name']}...")
    try:
        results = tavily.search(query=query, search_depth="advanced", max_results=3)
        context = "\n".join([r['content'] for r in results['results']])
    except Exception as e:
        context = "Research failed. Relying on provided description."
        
    return {"research_data": context}

# WRITER AGENTS (The "Critique" Logic is embedded) 

def generate_content(role: str, platform_rules: str, state_data: str, research: str):
    """
    Generic function to generate content with a built-in critique loop.
    """
    prompt = ChatPromptTemplate.from_template(
        """
        You are an elite Social Media Manager specializing in {role}.
        
        PRODUCT CONTEXT:
        {research}
        
        USER NOTES:
        {state_data}
        
        YOUR TASK:
        Create content for {role} following these rules:
        {platform_rules}
        
        CRITICAL INSTRUCTION (INTERNAL MONOLOGUE):
        1. Draft the initial post.
        2. Critique it: Is it boring? Does it sound like generic AI? Is it "salesy" enough?
        3. Refine it: Make it punchy, human, and optimized for conversion. 
        4. Output ONLY the final refined version. Do not output the critique.
        """
    )
    chain = prompt | llm
    response = chain.invoke({
        "role": role,
        "research": research,
        "state_data": state_data,
        "platform_rules": platform_rules
    })
    return response.content

# Specific Platform Wrappers
def twitter_writer(state):
    # CHANGED: "Max 200 chars" gives us a safety buffer so we never hit the 280 limit.
    rules = "STRICT LIMIT: Must be under 200 characters. No hashtags. Tone: Punchy, contrarian, or witty. Do not use emojis." 
    content = generate_content("Twitter (X)", rules, state['product_description'], state['research_data'])
    return {"twitter_post": content}

def linkedin_writer(state):
    rules = "Tone: Professional, authoritative, educational. Focus on 'Lessons Learned' or 'Industry Shift'. Use bullet points. clear CTA. High value."
    content = generate_content("LinkedIn", rules, state['product_description'], state['research_data'])
    return {"linkedin_post": content}

def facebook_writer(state):
    rules = "Tone: Exciting, community-focused, slightly more casual. Focus on the 'Hype' and the 'Solution'. Engage the reader with a question."
    content = generate_content("Facebook", rules, state['product_description'], state['research_data'])
    return {"facebook_post": content}

def instagram_writer(state):
    rules = "Output format: 1. Visual Description (What to film), 2. Audio Script (What to say), 3. Caption (for the post). Tone: Visual, aesthetic, trending."
    content = generate_content("Instagram Reels", rules, state['product_description'], state['research_data'])
    return {"instagram_post": content}