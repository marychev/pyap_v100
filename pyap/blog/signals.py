

def save_comment(sender, instance, created, **kwargs):
    if created:
        comment = instance
        post = comment.post
        post.comment_count = post.comment_set.count()
        post.save(force_update=True)
