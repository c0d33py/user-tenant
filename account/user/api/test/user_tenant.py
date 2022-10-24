# 1 - User Tenant Configration
# 2 - User Tenant List Configration
# 3 - User Tenant Create Configration
# 4 - User Tenant Update Configration
# 5 - User Tenant Detail Configration
# 6 - User Tenant Delete Configration


class UserTenantConfigSerializer(serializers.ModelSerializer):
    ''' User tenant config serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserTenantConfigListSerializer(serializers.ModelSerializer):
    ''' User tenant config list serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserTenantConfigCreateSerializer(serializers.ModelSerializer):
    ''' User tenant config create serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserTenantConfigUpdateSerializer(serializers.ModelSerializer):
    ''' User tenant config update serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserTenantConfigDetailSerializer(serializers.ModelSerializer):
    ''' User tenant config detail serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserTenantConfigDeleteSerializer(serializers.ModelSerializer):
    ''' User tenant config delete serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
