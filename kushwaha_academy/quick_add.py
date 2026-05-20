# Ek simple admin script banakar content add karo
cat > quick_add.py << 'EOF'
from app import app, db
from models import Article, Blog, Story

with app.app_context():
    # Add an article
    article = Article(
        title="Welcome to Kushwaha Academy",
        category="education",
        language="english",
        thumbnail="default_article.jpg",
        content="""
# Welcome to Kushwaha Academy!

We are excited to have you here. Start your learning journey today!

## What we offer:
- Quality articles
- Informative blogs
- Inspiring stories
- NISM mock tests
- Video courses

Happy Learning! 🚀
        """
    )
    db.session.add(article)
    db.session.commit()
    print("✅ Sample article added!")

    # Add a blog
    blog = Blog(
        title="Why Continuous Learning Matters",
        category="education",
        language="english",
        thumbnail="default_blog.jpg",
        content="""
# Why Continuous Learning Matters

In today's fast-paced world, continuous learning is not optional - it's essential.

## Benefits of Lifelong Learning:
1. **Career Growth** - Better opportunities
2. **Personal Development** - Confidence boost
3. **Adaptability** - Stay relevant
4. **Networking** - Meet like-minded people

Keep learning, keep growing! 🌱
        """
    )
    db.session.add(blog)
    db.session.commit()
    print("✅ Sample blog added!")

    # Add a story
    story = Story(
        title="The Power of Perseverance",
        category="education",
        language="english",
        thumbnail="default_story.jpg",
        content="""
# The Power of Perseverance

A true story about never giving up.

## The Challenge
When everything seemed impossible, she kept going.

## The Journey
Every failure taught her something new.

## The Success
Today, she runs her own successful business.

Remember: Success is not final, failure is not fatal - it's the courage to continue that counts. 💪
        """
    )
    db.session.add(story)
    db.session.commit()
    print("✅ Sample story added!")

print("\n✨ All content added successfully!")
print("Visit: http://localhost:5000/articles")
print("Visit: http://localhost:5000/blogs")
print("Visit: http://localhost:5000/stories")
EOF

python3 quick_add.py