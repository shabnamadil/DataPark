from rest_framework import serializers
from apps.community.models import (
    ChiefDataOfficers,
    TalentPool,
    TalentLevel,
    TalentPosition,
    TalentSector
)



class CDOListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiefDataOfficers
        fields = (
            'id',
            'full_name',
            'image',
            'position',
            'company',
            'linkedin_url'
        )


class CDOPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiefDataOfficers
        fields = (
        'name',
        'surname',
        'image',
        'position',
        'company',
        'linkedin_url'
    )
        

class TalentPositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentPosition
        fields = (
            'id',
            'position_name',
            'slug'
        )


class TalentLevelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentLevel
        fields = (
            'id',
            'level_name',
            'slug'
        )


class TalentSectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentSector
        fields = (
            'id',
            'sector_name',
            'slug'
        )


class TalentPoolListSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    class Meta:
        model = TalentPool
        fields = (
            'id',
            'full_name',
            'image',
            'position',
            'company',
            'linkedin_url'
        )

    def get_position(self, obj):
        return obj.position.position_name


class TalentPoolPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentPool
        fields = (
        'name',
        'surname',
        'image',
        'position',
        'sector',
        'level',
        'company',
        'work_location',
        'job_type',
        'linkedin_url'
    )