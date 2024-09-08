import time, random
from celery import shared_task
# from .. import db
from ..models import User, Post

# bind is used to provide access to the task instance, useful to retries or aborting tasks
@shared_task(bind=True, ignore_results=False, max_retries=3)
def get_user_posts(self, user_id: int):
    try:
        time.sleep(random.randint(10, 30))
        user = User.query.filter(User.id==user_id).first()
        user_posts = Post.query.filter(Post.user_id==user.id).all()
        post_list = [p.to_dict() for p in user_posts]
        return {'user': user.to_dict(), 'posts': post_list}
    
    except Exception as e:
        print(f"EXCEPTION -> {e}")
        # retrying after 3 seconds
        self.retry(countdown=3)
    
       
    
        
     