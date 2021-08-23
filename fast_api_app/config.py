from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Meu app bom"
    admin_email: str
    items_per_user: int = 50
