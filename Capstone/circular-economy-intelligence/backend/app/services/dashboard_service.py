from sqlalchemy.orm import Session

from backend.app.database.crud import (
    dashboard_stats,
    material_distribution,
    recent_analyses,
)


def get_dashboard_data(
    db: Session
):
    stats = dashboard_stats(db)

    distribution = material_distribution(
        db
    )

    recent = recent_analyses(
        db,
        limit=10
    )

    return {
        "stats": stats,
        "material_distribution": distribution,
        "recent_analyses": recent,
    }