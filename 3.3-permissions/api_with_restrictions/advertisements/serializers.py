from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context["request"].user
        new_status = data.get('status', AdvertisementStatusChoices.OPEN)

        if new_status == AdvertisementStatusChoices.OPEN:
            open_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
                ).count()
            
            if self.instance is None or self.instance.status == AdvertisementStatusChoices.CLOSED:
                print(open_count)
                if open_count >= 10:
                    raise serializers.ValidationError({
                        'status': 'Нельзя создать больше 10 открытых объявлений'
                    })

        return data

class FavoriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Favorite
        fields = ['id', 'creator', 'advertisement', 'created_at']
        read_only_fields = ['creator', 'created_at']