from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.utils import is_user_auth


class AbstractVoteSerializer(serializers.ModelSerializer):
    def create_or_update_vote(self, instance, vote):
        instance_dict = {self.Meta.key_containing_rating: instance}
        request = self.context.get("request")
        if is_user_auth(request):
            user = request.user
            vote = int(vote) % 6
            current_vote = self.Meta.model.objects.filter(user=user, **instance_dict)
            if current_vote.count() > 0:
                current_vote = current_vote[0]
                current_vote.rating = vote
                current_vote.save()
            else:
                current_vote = self.Meta.model.objects.create(user=user, rating=vote, **instance_dict)
            instance.rating = instance.rating_calculated
            instance.save()
            return current_vote
        raise ValidationError(f"You need to be logged in to vote for a {self.Meta.key_containing_rating}!")

    def create(self, validated_data):
        return self.create_or_update_vote(validated_data.get(self.Meta.key_containing_rating),
                                          validated_data.get("rating"))

    def update(self, instance, validated_data):
        return self.create_or_update_vote(validated_data.get(self.Meta.key_containing_rating),
                                          validated_data.get("rating"))