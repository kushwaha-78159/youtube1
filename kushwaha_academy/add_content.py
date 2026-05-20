cat > add_content.py << 'EOF'
from app import app, db
from models import Article, Blog, Story
from datetime import datetime

# ============== ARTICLE ADD KARNE KA EXAMPLE ==============
def add_sample_article():
    with app.app_context():
        article = Article(
            title="Python Programming for Beginners",
            category="tech",
            language="english",
            thumbnail="python.jpg",  # Apni image ka naam
            content="""
# Python Programming for Beginners

Python is a powerful programming language that is easy to learn.

## Why Learn Python?

- Easy to read and write
- Huge community support
- Great for beginners
- Used in AI, Web Development, Data Science

## Getting Started

```python
print("Hello, World!")