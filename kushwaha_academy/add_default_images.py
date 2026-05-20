# 1. Upload folder mein images daalo
# Folder location: static/uploads/

# 2. Default thumbnails create karo (agar image nahi hai to)
cat > add_default_images.py << 'EOF'
from PIL import Image, ImageDraw, ImageFont
import os

def create_default_thumbnail(filename, title, color):
    img = Image.new('RGB', (600, 400), color=color)
    draw = ImageDraw.Draw(img)
    
    # Text add karo
    draw.text((50, 180), title, fill='white', font=None)
    
    img.save(f'static/uploads/{filename}')
    print(f"Created: {filename}")

# Default images create karo
create_default_thumbnail('default_article.jpg', 'Article', '#4F46E5')
create_default_thumbnail('default_blog.jpg', 'Blog', '#10B981')
create_default_thumbnail('default_story.jpg', 'Story', '#F59E0B')
EOF

python3 add_default_images.py