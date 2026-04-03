from collections import Counter
from services.sales_service import get_sales
from services.books_service import get_book_by_id

def most_sold_books():
    sales = get_sales()

    if not sales:
        return []
    
    book_ids = [sale['book_id'] for sale in sales]
    counter = Counter(book_ids)

    results = []
    book_cache = {}
    
    for book_id, count in counter.most_common(5):
        if book_id not in book_cache:
            book_cache[book_id] = get_book_by_id(book_id)

        book = book_cache[book_id]

        results.append({
            "book_id": book_id,
            "title": book['title'] if book else "Unknown",
            "total_sales": count
        })
    
    return results


def total_sales():
    sales = get_sales()
    
    return {
        "total_sales": len(sales)
    }


def total_revenue():
    sales = get_sales()
    
    total_amount = sum(sale.get('amount', 0) for sale in sales)
    
    return {
        "total_revenue": total_amount
    }