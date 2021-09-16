from rest_framework import serializers

from .models import CheckRequest, SingleCheckRequest, WebSite, WebSiteCheckRequest


class WebSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSite
        fields = "__all__"


class WebSiteCheckRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSiteCheckRequest
        fields = "__all__"


class SingleCheckRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleCheckRequest
        fields = "__all__"


class CheckRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckRequest
        fields = "__all__"
