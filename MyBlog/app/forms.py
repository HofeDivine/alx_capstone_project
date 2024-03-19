
from app.models import CreateBlog  

# Query to retrieve all blog po
blogs = CreateBlog.query.all()

# Loop through each blog post and print its id and title
for blog in blogs:
    print(f"Blog ID: {blog.id}, Title: {blog.title}")
