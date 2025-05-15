import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from trend_analyzer import get_youtube_music_trends  # Importing the trend analyzer

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI Chat Model via LangChain
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)

# Define the prompt template for generating content
prompt_template = PromptTemplate(
    input_variables=["song_title", "platform", "tone", "length", "hashtags"],
    template="""
    Write a {length} post for {platform} about the song "{song_title}" with the following tone:
    
    - Tone: {tone}
    - Hashtags: {hashtags}
    
    The post should be engaging, clear, and concise, and it should fit the typical style of {platform}. Keep the length under {length} words. The tone and content should be appropriate for the {platform} platform.
    """
)

# Platform-specific guidelines for generating the posts
def platform_style(platform):
    if platform == 'twitter':
        return "Keep it concise, under 280 characters. Twitter is all about quick, catchy, and sharable content."
    elif platform == 'instagram':
        return "Instagram posts should be engaging, with a balance of casual language and professionalism. Use hashtags creatively."
    elif platform == 'tiktok':
        return "TikTok content is often more fun, casual, and energetic. Focus on making the post catchy and relatable."
    elif platform == 'blog post':
        return "A blog post can be longer and more detailed. Focus on providing value and creating an engaging narrative."
    else:
        return "Keep it suitable for the chosen platform, keeping in mind its unique style and tone."

# Function to generate content based on trending data
def generate_content_from_trends(song_title, platform, tone="neutral", length="short", hashtags=[]):
    # Adjusting word limits based on the length
    word_limit = 50 if length == "short" else 150 if length == "medium" else 300 if length == "long" else 50

    # Get platform-specific guidelines
    platform_guide = platform_style(platform)

    # Create the prompt dynamically
    prompt = prompt_template.format(
        song_title=song_title,
        platform=platform,
        tone=tone,
        length=length,
        hashtags=", ".join(hashtags)
    )
    
    # Add the platform-specific style to the prompt
    prompt += f" {platform_guide}"
    
    # Generate content using the OpenAI model
    response = llm.invoke(prompt)  # Model response
    content = response.content if hasattr(response, 'content') else str(response)  # Access content
    
    # Enforce the word limit based on user selection
    content_words = content.split()
    content = " ".join(content_words[:word_limit])  # Limit to the set number of words
    
    return content

# Function to fetch trending data from `trend_analyzer.py`
def fetch_trending_data():
    trending_hashtags, trending_videos = get_youtube_music_trends()  # Fetch data from trend_analyzer
    
    # Get the most common hashtags
    return trending_hashtags, [video[0] for video in trending_videos]  # Titles of the trending songs

# Main execution to generate content based on trends
def analyze_and_generate_content():
    topic = "Song Highlight"  # Example topic for the content
    print("Fetching trends and generating content...\n")

    # Fetch trending data from YouTube
    trending_hashtags, trending_songs = fetch_trending_data()

    print("\nTrending Songs:")
    for index, song in enumerate(trending_songs, start=1):
        print(f"{index}. {song}")
    
    # Ask the user to select a song
    song_index = int(input("\nSelect a song by number to generate content: ")) - 1
    selected_song = trending_songs[song_index]
    
    # Ask for other parameters: tone, length, platform
    tone = input("\nEnter the tone (e.g., 'neutral', 'energetic', 'funny'): ").lower()
    length = input("\nEnter the length (e.g., 'short', 'medium', 'long'): ").lower()
    platform = input("\nSelect the platform (e.g., 'Twitter', 'Instagram', 'TikTok', 'Blog Post'): ").lower()

    # Generate content based on the selected song and parameters
    try:
        content = generate_content_from_trends(
            song_title=selected_song,
            platform=platform,
            tone=tone,
            length=length,
            hashtags=trending_hashtags  # Include trending hashtags
        )
        print("\nGenerated Content:\n")
        print(content)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_and_generate_content()

# Run python3 -u "/Users/thomasnielsen/Documents/someapp/some.py"
