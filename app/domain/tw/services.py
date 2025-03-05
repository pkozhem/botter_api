import httpx

from app.config import get_settings


class TwitchOauth2Login:
    settings = get_settings()

    @classmethod
    def get_body(cls) -> dict:
        return {
            "client_id": cls.settings.client_id,
            "client_secret": cls.settings.client_secret,
            "grant_type": 'client_credentials',
        }

    async def perform_request(self):
        with httpx.AsyncClient as client:
            response = await client.post(
                url="https://id.twitch.tv/oauth2/token",
                data=self.get_body(),
            )
            print(response)
