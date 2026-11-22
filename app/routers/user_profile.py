from fastapi import APIRouter, Depends, HTTPException, status

from app.routers.dependencies import get_user_profile_service
from app.schemas.user_profile import NutritionTargets, UserProfileCreate, UserProfileRead
from app.services.user_profile_service import UserProfileService


router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("", response_model=UserProfileRead)
def get_profile(service: UserProfileService = Depends(get_user_profile_service)) -> UserProfileRead:
    profile = service.get_current()
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User profile not set")
    return UserProfileRead.model_validate(profile)


@router.put("", response_model=UserProfileRead)
def save_profile(
    payload: UserProfileCreate,
    service: UserProfileService = Depends(get_user_profile_service),
) -> UserProfileRead:
    return UserProfileRead.model_validate(service.save(payload))


@router.get("/targets", response_model=NutritionTargets)
def get_targets(
    service: UserProfileService = Depends(get_user_profile_service),
) -> NutritionTargets:
    profile = service.get_current()
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User profile not set")
    return service.compute_targets(profile)
