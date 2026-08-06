def max_boook(book_w, shelf_l):
    total = 0
    c = 0
    #sort
    book_w.sort()

    for widht in book_w:
        if total + widht <= shelf_l:
            total += widht
            c += 1
        else:
            break
    return c

books = [3, 8, 5, 1, 7]
lenght = 10
books_2 = [12, 15, 7]
lenght_2 = 6
print(max_boook(books, lenght))
print(max_boook(books_2, lenght_2))

    