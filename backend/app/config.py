from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://mi_tienda:mi_tienda_dev@db:5432/mi_tienda"
    secret_key: str = "cambiar-esta-clave-en-produccion"
    first_admin_email: str = "admin@mitienda.local"
    first_admin_password: str = "Admin123!"
    access_token_minutes: int = 480
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

