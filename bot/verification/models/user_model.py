from typing import cast

class User:
    def __init__(self, email: str, username: str):
        self.email = email
        self.username = username
    
    @classmethod
    def from_dict(cls, data: dict):
        assert "email" in data, "Email not found while creating user class"
        assert "username" in data, "Username not found while creating user class"
        
        return cls(
            cast(str, data["email"]),
            cast(str, data["username"])
        )

    def to_dict(self):
        return {
            "email": self.email,
            "username": self.username
        }

