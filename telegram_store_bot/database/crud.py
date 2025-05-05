# database/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .models import Order, Referral

async def get_user_orders(session: AsyncSession, user_id: int):
    """
    Get a user's order history
    Args:
        session: Async database session
        user_id: Telegram user ID
    Returns:
        List of Order objects
    """
    try:
        result = await session.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .limit(10)
        )
        return result.scalars().all()
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return []

async def get_user_referrals(session: AsyncSession, user_id: int):
    """
    Get a user's referral history
    Args:
        session: Async database session
        user_id: Telegram user ID
    Returns:
        List of Referral objects
    """
    try:
        result = await session.execute(
            select(Referral)
            .where(Referral.referrer_id == user_id)
            .order_by(Referral.created_at.desc())
        )
        return result.scalars().all()
    except Exception as e:
        print(f"Error fetching referrals: {e}")
        return []