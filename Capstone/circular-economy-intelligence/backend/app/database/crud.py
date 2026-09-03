from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.models.database_models import (
    User,
    WasteAnalysis,
)


# ============================================================
# USER OPERATIONS
# ============================================================

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    email: str,
    password_hash: str,
    name: str
):
    user = User(
        email=email,
        password_hash=password_hash,
        name=name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ============================================================
# WASTE ANALYSIS OPERATIONS
# ============================================================

def create_waste_analysis(
    db: Session,
    material: str,
    confidence: float,
    weight_kg: float,
    estimated_value: float,
    recommendation: str,
    image_path: str,
):
    analysis = WasteAnalysis(
        material=material,
        confidence=confidence,
        weight_kg=weight_kg,
        estimated_value=estimated_value,
        recommendation=recommendation,
        image_path=image_path,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def dashboard_stats(
    db: Session
):
    total = (
        db.query(
            func.count(WasteAnalysis.id)
        ).scalar()
        or 0
    )

    recyclable_materials = [
        "paper",
        "cardboard",
        "plastic",
        "metal",
        "white-glass",
        "green-glass",
        "brown-glass",
        "battery",
        "clothes",
        "shoes",
    ]

    recyclable = (
        db.query(WasteAnalysis)
        .filter(
            WasteAnalysis.material.in_(
                recyclable_materials
            )
        )
        .count()
    )

    non_recyclable = (
        total - recyclable
    )

    value = (
        db.query(
            func.coalesce(
                func.sum(
                    WasteAnalysis.estimated_value
                ),
                0.0,
            )
        ).scalar()
        or 0.0
    )

    total_weight = (
        db.query(
            func.coalesce(
                func.sum(
                    WasteAnalysis.weight_kg
                ),
                0.0,
            )
        ).scalar()
        or 0.0
    )

    recyclable_percentage = (
        (recyclable / total * 100)
        if total > 0
        else 0.0
    )

    return {
        "total_analyses": total,
        "recyclable_analyses": recyclable,
        "non_recyclable_analyses": non_recyclable,
        "recyclable_percentage": round(
            recyclable_percentage,
            2
        ),
        "total_weight_kg": round(
            float(total_weight),
            2
        ),
        "estimated_value": round(
            float(value),
            2
        ),
        "currency": "INR",
    }


# ============================================================
# MATERIAL DISTRIBUTION
# ============================================================

def material_distribution(
    db: Session
):
    rows = (
        db.query(
            WasteAnalysis.material,
            func.count(WasteAnalysis.id)
        )
        .group_by(
            WasteAnalysis.material
        )
        .order_by(
            func.count(
                WasteAnalysis.id
            ).desc()
        )
        .all()
    )

    return [
        {
            "material": material,
            "count": count,
        }
        for material, count in rows
    ]


# ============================================================
# RECENT ANALYSES
# ============================================================

def recent_analyses(
    db: Session,
    limit: int = 10
):
    rows = (
        db.query(WasteAnalysis)
        .order_by(
            WasteAnalysis.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "id": row.id,
            "material": row.material,
            "confidence": row.confidence,
            "weight_kg": row.weight_kg,
            "estimated_value": row.estimated_value,
            "recommendation": row.recommendation,
            "created_at": (
                row.created_at.isoformat()
                if row.created_at
                else None
            ),
        }
        for row in rows
    ]

    # ============================================================
# ANALYSIS HISTORY
# ============================================================

def analysis_history(
    db: Session,
    limit: int = 100
):
    rows = (
        db.query(WasteAnalysis)
        .order_by(
            WasteAnalysis.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "id": row.id,
            "material": row.material,
            "confidence": row.confidence,
            "weight_kg": row.weight_kg,
            "estimated_value": row.estimated_value,
            "recommendation": row.recommendation,
            "image_path": row.image_path,
            "created_at": (
                row.created_at.isoformat()
                if row.created_at
                else None
            ),
        }
        for row in rows
    ]