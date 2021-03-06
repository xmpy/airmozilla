from django.db import models
from django.contrib.auth.models import User

from airmozilla.main.models import Event, SuggestedEvent


class Comment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, null=True)
    comment = models.TextField()
    reply_to = models.ForeignKey('self', related_name='parent', null=True)

    STATUS_POSTED = 'posted'
    STATUS_APPROVED = 'approved'
    STATUS_REMOVED = 'removed'
    STATUS_CHOICES = (
        (STATUS_POSTED, 'Posted'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REMOVED, 'Removed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=STATUS_POSTED)
    flagged = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def anonymous(self):
        return not self.user_id


#class CommentVotes(models.Model):
#    comment = models.ForeignKey(Comment)
#    vote = models.IntegerField(default=1)
#    created = models.DateTimeField(auto_now_add=True)


class Discussion(models.Model):
    event = models.ForeignKey(Event, unique=True)
    enabled = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    moderate_all = models.BooleanField(default=False)
    notify_all = models.BooleanField(default=False)
    moderators = models.ManyToManyField(User, related_name='moderators')


class SuggestedDiscussion(models.Model):
    event = models.ForeignKey(SuggestedEvent, unique=True)
    enabled = models.BooleanField(default=False)
    moderate_all = models.BooleanField(default=False)
    notify_all = models.BooleanField(default=False)
    moderators = models.ManyToManyField(
        User,
        related_name='suggested_moderators'
    )


class Unsubscription(models.Model):
    user = models.ForeignKey(User)
    discussion = models.ForeignKey(Discussion, null=True)
    created = models.DateTimeField(auto_now_add=True)
