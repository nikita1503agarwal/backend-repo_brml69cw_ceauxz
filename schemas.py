"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Class name lowercased = collection name.
"""
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List

class Briefrequest(BaseModel):
    brand_name: str = Field(..., description="Brand or artist name")
    contact_name: str = Field(..., description="Primary contact name")
    email: EmailStr = Field(..., description="Contact email")
    instagram: Optional[str] = Field(None, description="Instagram handle")
    website: Optional[HttpUrl] = Field(None, description="Website URL")
    budget_range: Optional[str] = Field(None, description="Estimated budget range")
    timeline: Optional[str] = Field(None, description="Desired timeline")
    brief: str = Field(..., description="Project description / brief")
    consent: bool = Field(True, description="Consent to be contacted")

class Creatorapplication(BaseModel):
    name: str = Field(..., description="Creator full name or alias")
    email: EmailStr = Field(..., description="Email address")
    discipline: str = Field(..., description="Primary craft e.g. photo, film, design")
    location: Optional[str] = Field(None, description="City, Country")
    portfolio_url: Optional[HttpUrl] = Field(None, description="Portfolio or linktree")
    socials: Optional[str] = Field(None, description="Key social handles")
    bio: Optional[str] = Field(None, description="Short bio")
    interests: Optional[List[str]] = Field(None, description="Tags or interests")

class Subscriber(BaseModel):
    email: EmailStr = Field(..., description="Subscriber email")
    source: Optional[str] = Field(None, description="Signup source")

# Example collections left for reference (not used by DSM directly)
class User(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
