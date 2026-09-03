from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Depends,
)

from sqlalchemy.orm import Session

from backend.app.services.image_service import (
    save_upload,
)

from backend.app.services.classification_service import (
    classify_image,
)

from backend.app.services.valuation_service import (
    estimate_value,
)

from backend.app.services.recommendation_service import (
    recommendation_for,
)

from backend.app.database.database import (
    get_db,
)

from backend.app.database.crud import (
    create_waste_analysis,
    analysis_history,
)


router = APIRouter()


@router.post("/analyze")
async def analyze_waste(
    file: UploadFile = File(...),
    weight_kg: float = Form(...),
    quality_factor: float = Form(1.0),
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # VALIDATE IMAGE
    # --------------------------------------------------------

    if (
        not file.content_type
        or not file.content_type.startswith(
            "image/"
        )
    ):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file.",
        )

    # --------------------------------------------------------
    # VALIDATE WEIGHT
    # --------------------------------------------------------

    if weight_kg <= 0:
        raise HTTPException(
            status_code=400,
            detail="weight_kg must be greater than 0.",
        )

    # --------------------------------------------------------
    # VALIDATE QUALITY FACTOR
    # --------------------------------------------------------

    if (
        quality_factor < 0
        or quality_factor > 1.2
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "quality_factor must be "
                "between 0 and 1.2."
            ),
        )

    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    try:
        path = await save_upload(file)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Unable to save uploaded image: {exc}"
            ),
        )

    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

    try:
        classification = classify_image(
            path
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Image classification failed: {exc}"
            ),
        )

    material = classification[
        "material"
    ]

    confidence = classification[
        "confidence"
    ]

    # --------------------------------------------------------
    # VALUATION
    # --------------------------------------------------------

    valuation = estimate_value(
        material=material,
        weight_kg=weight_kg,
        quality_factor=quality_factor,
    )

    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    recommendation = recommendation_for(
        material
    )

    # --------------------------------------------------------
    # SAVE ANALYSIS TO DATABASE
    # --------------------------------------------------------

    try:

        saved_analysis = create_waste_analysis(
            db=db,
            material=material,
            confidence=confidence,
            weight_kg=weight_kg,
            estimated_value=(
                valuation["estimated_value"]
            ),
            recommendation=(
                recommendation["action"]
            ),
            image_path=str(path),
        )

    except Exception as exc:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                f"Unable to save analysis: {exc}"
            ),
        )

    # --------------------------------------------------------
    # COMPLETE RESPONSE
    # --------------------------------------------------------

    return {

        "analysis_id":
            saved_analysis.id,

        "filename":
            Path(path).name,

        "image_path":
            str(path),

        # Classification
        "material":
            material,

        "confidence":
            confidence,

        "top_predictions":
            classification[
                "top_predictions"
            ],

        "recyclable":
            classification[
                "recyclable"
            ],

        # Quantity
        "weight_kg":
            weight_kg,

        # Valuation
        "rate_per_kg":
            valuation[
                "rate_per_kg"
            ],

        "quality_factor":
            quality_factor,

        "estimated_value":
            valuation[
                "estimated_value"
            ],

        "currency":
            valuation[
                "currency"
            ],

        # Recommendation
        "recommendation":
            recommendation[
                "action"
            ],

        "recommendation_detail":
            recommendation[
                "detail"
            ],

        # Database
        "created_at":
            (
                saved_analysis.created_at.isoformat()
                if saved_analysis.created_at
                else None
            ),

        "status":
            "success",
    }

    # ============================================================
# ANALYSIS HISTORY
# ============================================================

@router.get("/history")
def get_history(
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if limit < 1 or limit > 500:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 500.",
        )

    analyses = analysis_history(
        db,
        limit
    )

    return {
        "count": len(analyses),
        "analyses": analyses,
    }