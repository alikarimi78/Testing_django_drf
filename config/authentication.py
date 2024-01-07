from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import CustomToken  # Assuming you have a CustomToken model


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        is_legal = validated_token.get("is_legal", False)
        user_id = validated_token["user_id"]
        user = self.user_model.objects.filter(id=user_id).first()
        company = None

        if not user:
            raise AuthenticationFailed("User not exist", code="user_inactive")
        if is_legal:
            company = user.sub_user.posts.filter(post_type="001").first().company_person.company
            if not company:
                raise users_exceptions.NotLegalUser()

        if not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")

        return user, is_legal, company

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user, is_legal, company = self.get_user(validated_token)

        # Check for existing active tokens for the user
        existing_tokens = CustomToken.objects.filter(user=user, is_active=True).exclude(token=str(raw_token))
        if existing_tokens.exists():
            # Invalidate existing tokens
            existing_tokens.update(is_active=False)
            raise AuthenticationFailed("Multiple logins not allowed", code="multiple_logins")

        # Create a new entry for the current token
        CustomToken.objects.create(user=user, token=str(raw_token), is_active=True)

        request.is_legal = is_legal
        request.company = company
        return user, validated_token
