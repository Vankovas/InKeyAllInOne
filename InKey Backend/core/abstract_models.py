from django.db import models


class AbstractVote(models.Model):
    key_containing_rating = "string"
    rating = models.IntegerField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        instance = super(AbstractVote, self).save(*args, **kwargs)
        rate_saving_instance = getattr(self, self.key_containing_rating)
        rate_saving_instance.rating = rate_saving_instance.rating_calculated
        rate_saving_instance.save()
        return instance


class AbstractViewsRatingAndCreatedTime(models.Model):
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    class Meta:
        abstract = True

    @property
    def rating_calculated(self):
        all_votes = 0
        for vote in self.votes.all():
            all_votes += vote.rating
        if self.votes.count() > 0:
            return all_votes/self.votes.count()
        return 0