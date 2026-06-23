from uuid import UUID

from fastapi import Request, APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from src.domain.exceptions import ExportError
from src.application.commands import ExportNomenclatureCommand

router = APIRouter()


@router.get("/{job_id}/download")
async def download_nomenclature(request: Request, job_id: UUID) -> FileResponse:
    handler = request.app.state.export_handler

    try:
        export_path = await handler.execute(ExportNomenclatureCommand(job_id=job_id))

    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        ) from exc

    except ExportError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        ) from exc

    if not export_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Export file not found"
        )

    return FileResponse(
        path=export_path,
        filename=export_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
