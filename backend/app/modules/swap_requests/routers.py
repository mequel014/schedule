# ./app/modules/swap_requests/routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime

from app.core.db import get_session
from app.core.security import get_current_user, get_current_admin
from app.modules.users.models import User
from app.modules.shifts.models import Shift
from .models import SwapRequest, SwapRequestStatus, SwapRequestType
from .schemas import SwapRequestCreate, SwapRequestResolve, SwapRequestRead

router = APIRouter(prefix="/api/swap-requests", tags=["swap-requests"])


@router.get("", response_model=List[SwapRequestRead])
async def list_swap_requests(
    status: SwapRequestStatus = None,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """List all swap requests (admin only)"""
    statement = select(SwapRequest)
    if status:
        statement = statement.where(SwapRequest.status == status)
    
    requests = session.exec(statement.order_by(SwapRequest.created_at.desc())).all()
    
    result = []
    for req in requests:
        shift = session.get(Shift, req.shift_id)
        req_read = SwapRequestRead(
            id=req.id,
            requester_id=req.requester_id,
            requester_name=req.requester.full_name if req.requester else None,
            shift_id=req.shift_id,
            shift_date=str(shift.date) if shift else None,
            request_type=req.request_type,
            target_doctor_id=req.target_doctor_id,
            target_doctor_name=req.target_doctor.full_name if req.target_doctor else None,
            target_shift_id=req.target_shift_id,
            status=req.status,
            comment=req.comment,
            admin_comment=req.admin_comment,
            created_at=req.created_at,
            resolved_at=req.resolved_at
        )
        result.append(req_read)
    
    return result


@router.get("/me", response_model=List[SwapRequestRead])
async def get_my_swap_requests(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get my swap requests"""
    statement = select(SwapRequest).where(
        SwapRequest.requester_id == current_user.id
    ).order_by(SwapRequest.created_at.desc())
    
    requests = session.exec(statement).all()
    
    result = []
    for req in requests:
        shift = session.get(Shift, req.shift_id)
        result.append(SwapRequestRead(
            id=req.id,
            requester_id=req.requester_id,
            shift_id=req.shift_id,
            shift_date=str(shift.date) if shift else None,
            request_type=req.request_type,
            target_doctor_id=req.target_doctor_id,
            target_doctor_name=req.target_doctor.full_name if req.target_doctor else None,
            target_shift_id=req.target_shift_id,
            status=req.status,
            comment=req.comment,
            admin_comment=req.admin_comment,
            created_at=req.created_at,
            resolved_at=req.resolved_at
        ))
    
    return result


@router.post("", response_model=SwapRequestRead)
async def create_swap_request(
    data: SwapRequestCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a swap or cancel request"""
    # Verify shift exists and belongs to user
    shift = session.get(Shift, data.shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    if shift.doctor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your shift")
    
    # For swap, verify target shift exists
    if data.request_type == SwapRequestType.SWAP:
        if not data.target_doctor_id:
            raise HTTPException(status_code=400, detail="Target doctor required for swap")
    
    request = SwapRequest(
        requester_id=current_user.id,
        shift_id=data.shift_id,
        request_type=data.request_type,
        target_doctor_id=data.target_doctor_id,
        target_shift_id=data.target_shift_id,
        comment=data.comment
    )
    session.add(request)
    session.commit()
    session.refresh(request)
    
    return SwapRequestRead(
        id=request.id,
        requester_id=request.requester_id,
        shift_id=request.shift_id,
        shift_date=str(shift.date),
        request_type=request.request_type,
        target_doctor_id=request.target_doctor_id,
        target_shift_id=request.target_shift_id,
        status=request.status,
        comment=request.comment,
        admin_comment=request.admin_comment,
        created_at=request.created_at,
        resolved_at=request.resolved_at
    )


@router.patch("/{request_id}", response_model=SwapRequestRead)
async def resolve_swap_request(
    request_id: UUID,
    data: SwapRequestResolve,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Approve or reject a swap request"""
    request = session.get(SwapRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != SwapRequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Request already resolved")
    
    request.status = data.status
    request.admin_comment = data.admin_comment
    request.resolved_at = datetime.utcnow()
    
    # If approved, perform the swap/cancel
    if data.status == SwapRequestStatus.APPROVED:
        shift = session.get(Shift, request.shift_id)
        
        if request.request_type == SwapRequestType.CANCEL:
            # Delete the shift
            session.delete(shift)
        elif request.request_type == SwapRequestType.SWAP:
            # Swap doctors
            if request.target_shift_id:
                target_shift = session.get(Shift, request.target_shift_id)
                if target_shift:
                    # Swap both shifts
                    shift.doctor_id, target_shift.doctor_id = target_shift.doctor_id, shift.doctor_id
                    session.add(target_shift)
            else:
                # Just reassign this shift
                shift.doctor_id = request.target_doctor_id
            session.add(shift)
    
    session.add(request)
    session.commit()
    session.refresh(request)
    
    shift = session.get(Shift, request.shift_id)
    return SwapRequestRead(
        id=request.id,
        requester_id=request.requester_id,
        requester_name=request.requester.full_name if request.requester else None,
        shift_id=request.shift_id,
        shift_date=str(shift.date) if shift else None,
        request_type=request.request_type,
        target_doctor_id=request.target_doctor_id,
        target_doctor_name=request.target_doctor.full_name if request.target_doctor else None,
        target_shift_id=request.target_shift_id,
        status=request.status,
        comment=request.comment,
        admin_comment=request.admin_comment,
        created_at=request.created_at,
        resolved_at=request.resolved_at
    )