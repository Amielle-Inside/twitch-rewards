"""Request body for the token creation endpoint"""

from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class AuthenticationData(BaseModel):
    """Wraps the data required for validating the user"""

    code: str
