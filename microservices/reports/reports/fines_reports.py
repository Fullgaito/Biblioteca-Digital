from collections import Counter
from services.fines_service import get_fines

def users_with_most_fines():
    fines = get_fines()

    if not fines:
        return []

    user_ids = [fine['user_id'] for fine in fines]
    counter = Counter(user_ids)

    result = []

    for user_id, total in counter.most_common(5):
        result.append({
            "user_id": user_id,
            "total_fines": total
        })

    return result


def total_fines():
    fines = get_fines()

    return {
        "total_fines": len(fines)
    }


def total_fines_amount():
    fines = get_fines()

    total_amount = sum(fine.get('amount', 0) for fine in fines)

    return {
        "total_amount": total_amount
    }