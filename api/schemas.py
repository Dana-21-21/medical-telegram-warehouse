from pydantic import BaseModel


class TopProduct(BaseModel):
    product: str
    frequency: int


class ChannelActivity(BaseModel):
    channel_name: str
    total_posts: int


class SearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str


class VisualContent(BaseModel):
    channel_name: str
    total_images: int
