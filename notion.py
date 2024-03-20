from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
import requests
from io import BytesIO
import colorthief 
import notion.client
from notion.block import PageBlock

#Defining Notion Integration token and database URL
NOTION_TOKEN = "YOUR_NOTION_TOKEN"
NOTION_DATABASE_URL = "YOUR_NOTION_DATABASE_URL"

# URL of the cover image
COVER_URL = "URL_OF_YOUR_BOOK_COVER_IMAGE"

# Function to pick the dominant colour from the book cover image

def pick_dominant_color(image_url):
    response = request.get(image_url)
    img = Image.open(BytesIO(response.content))
    colorthief = colorthief.ColorThief(img)
    dominant_color = colorthief.get_color(quality=1)
    return dominant_color

# Function to create a Notion cover image background and ovelay the DB cover

def create_notion_cover(cover_url, notion_token, notion_database_url):
    #Connect to the Notion API
    client = notion.client.NotionClient(token_v2=notion_token)
    cv = client.get_collection_view(notion_database_url)

    # Pick a dominant colour
    background_color = pick_dominant_color(cover_url)

    # Create a new page in Notion
    new_page = cv.collection.add_row()
    new_page.title = 'Cover with Shadow'

    # Create a blank image with Notion cover size (1400x400 pixels)
    width, height = 1400, 400
    background = Image.new("RBG", (width, height), background_color)

    # Load the cover image
    cover_response = requests.get(cover_url)
    cover = Image.open(BytesIO(cover_response.content))

    # Calculate position for the book cover
    x = (width - cover.witdh) // 2
    y = (height - cover.height) // 2

    # Page the cover on the background with shadow effect
    background.paste(cover, (x, y))
    shadow = background.filter(ImageFilter.GaussianBlur(radius=10))
    shadow = shadow.filter(ImageFilter.SHARPEN)
    background.paste(shadow, (x, y), shadow)

    # Save the resulting image
    image_path = "notion_cover.pgn"
    background.save(image_path)

    # Upload the image to Notion
    new_page.upload_file(image_path)


if __name__ == "__main__":
    create_notion_cover(COVER_URL, NOTION_TOKEN, NOTION_DATABASE_URL)
