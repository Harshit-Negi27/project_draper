from typing import TypedDict, Optional

class AgentState(TypedDict):
    product_name: str
    product_url: Optional[str]
    product_description: str
    
    # Context populated by Research Node
    research_data: Optional[str]
    
    # Outputs populated by Writer Nodes
    twitter_post: Optional[str]
    linkedin_post: Optional[str]
    facebook_post: Optional[str]
    instagram_post: Optional[str]