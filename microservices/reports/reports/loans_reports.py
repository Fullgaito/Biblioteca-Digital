from collections import Counter
from services.loans_service import get_loans
from services.books_service import get_book_by_id

def most_borrowed_books():
    loans=get_loans()

    if not loans:
        return []
    book_ids=[loan['book_id'] for loan in loans]
    counter=Counter(book_ids)

    results=[]
    book_cache={}
    for book_id, count in counter.most_common(5):

        if book_id not in book_cache:
            book_cache[book_id]=get_book_by_id(book_id)

        book=book_cache[book_id]

        results.append({
            "book_id": book_id,
            "title": book['title'] if book else "Unknown",
            "total loans": count
        })
    return results

def total_loans():
    loans=get_loans()
    return{
        "total_loans": len(loans) 
    }
    
