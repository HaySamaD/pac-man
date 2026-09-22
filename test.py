from pydantic import BaseModel, Field, ValidationError


class UserConfig(BaseModel):
    username: str = "guest"
    volume: int = Field(default=50, ge=0, le=100)
    is_active: bool = True


raw_data = {
            "username": "sannaka",
            "volume": 150,
           }

try:

    config = UserConfig(**raw_data)

except ValidationError as e:

    print(e)
    config = UserConfig()

print(config)
