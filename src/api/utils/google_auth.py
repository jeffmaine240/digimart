from src.api.core.config import config
from authlib.integrations.starlette_client import OAuth


class OAuthSettings:
    """
    Centralized OAuth Configuration Management
    """
    GOOGLE_CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

    @classmethod
    def get_google_oauth_client(self):
        """
        Create and configure Google OAuth client
        """
        oauth = OAuth()
        oauth.register(name="google",
                       client_id=config.GOOGLE_CLIENT_ID,
                       client_secret=config.GOOGLE_CLIENT_SECRET,
                       server_metadata_url=self.GOOGLE_CONF_URL,
                       client_kwargs={
                           "scope": ["openid", "email", "profile"],
                           "access_type": "offline",
                           "prompt": "consent"
                       })
        return oauth