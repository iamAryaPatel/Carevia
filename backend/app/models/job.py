"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime


class JobBase(BaseModel):
    """Base job model with common fields."""
    title: str = Field(..., min_length=1, max_length=500, description="Job title")
    company: str = Field(..., min_length=1, max_length=200, description="Company name")
    location: str = Field(..., min_length=1, max_length=200, description="Job location")
    category: Optional[str] = Field(None, max_length=100, description="Job category")
    url: HttpUrl = Field(..., description="Job application URL")
    source: str = Field(..., min_length=1, max_length=50, description="Job source platform")


class JobCreate(JobBase):
    """Model for creating a new job."""
    pass


class JobResponse(JobBase):
    """Model for job response with additional fields."""
    created_at: Optional[datetime] = Field(None, description="Job creation timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "Senior Python Developer",
                "company": "Tech Corp",
                "location": "Remote",
                "category": "Software Development",
                "url": "https://example.com/jobs/123",
                "source": "Remotive",
                "created_at": "2026-02-07T12:00:00"
            }
        }


class JobListResponse(BaseModel):
    """Model for paginated job list response."""
    jobs: list[JobResponse]
    total: int
    page: int
    page_size: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "jobs": [],
                "total": 100,
                "page": 1,
                "page_size": 20
            }
        }


class FetchJobsResponse(BaseModel):
    """Model for job fetch operation response."""
    inserted: int = Field(..., description="Number of new jobs inserted")
    total_fetched: int = Field(..., description="Total jobs fetched from sources")
    duplicates_skipped: int = Field(..., description="Number of duplicate jobs skipped")
    
    class Config:
        json_schema_extra = {
            "example": {
                "inserted": 15,
                "total_fetched": 50,
                "duplicates_skipped": 35
            }
        }


class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str
    database: str
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "database": "connected",
                "timestamp": "2026-02-07T12:00:00"
            }
        }
