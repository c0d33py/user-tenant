
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    ''' User login serializer '''

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data['password']
        if not username:
            raise serializers.ValidationError('A username is required to login.')
        user = User.objects.filter(username=username)
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError('This username is not valid.')
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError('Incorrect credentials please try again.')
        data['user'] = user_obj
        return data


class ProfileSerializer(serializers.ModelSerializer):
    ''' Profile serializer '''

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserChangePasswordSerializer(serializers.ModelSerializer):
    ''' User change password serializer '''

    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user_obj = None
        password = data['password']
        user = User.objects.filter(username=self.context['request'].user)
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError('This username is not valid.')
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError('Incorrect credentials please try again.')
        data['user'] = user_obj
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    ''' User update serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserDeleteSerializer(serializers.ModelSerializer):
    ''' User delete serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


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


class UserTwoFactorAuthSerializer(serializers.ModelSerializer):
    ''' User two factor auth serializer '''

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
