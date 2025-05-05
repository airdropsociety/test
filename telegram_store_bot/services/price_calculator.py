from decimal import Decimal

STAR_PRICE_USDT = Decimal('0.017')

async def calculate_stars_to_currency(stars: int) -> tuple[Decimal, Decimal]:
    """Calculate USDT and TON equivalent for given stars"""
    usdt = stars * STAR_PRICE_USDT
    # TODO: Add TON price conversion from API
    ton = usdt * Decimal('1.0')  # Placeholder - replace with actual conversion
    return usdt, ton

async def calculate_currency_to_stars(amount: Decimal) -> int:
    """Calculate how many stars can be bought for given currency amount"""
    return int(amount / STAR_PRICE_USDT)