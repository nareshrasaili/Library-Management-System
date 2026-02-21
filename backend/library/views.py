from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction
import json

# ================== LIBRARIAN LOGIN ==================
@csrf_exempt
def librarian_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM librarian WHERE email = %s", [email])
            row = cursor.fetchone()

        if not row:
            return JsonResponse({"message": "User not found"}, status=404)

        if row[0] == password:
            return JsonResponse({"message": "Login success"})
        else:
            return JsonResponse({"message": "Wrong password"}, status=401)

    return JsonResponse({"message": "Invalid request"}, status=400)


# ================== BOOK MANAGEMENT ==================
@csrf_exempt
def add_book(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        author_name = data.get("author")
        total_copies = data.get("total_copies")
        book_number = data.get("book_number")

        if not title or not author_name or not total_copies or not book_number:
            return JsonResponse({"message": "All fields required"}, status=400)

        with connection.cursor() as cursor:
            # Book number exists?
            cursor.execute("SELECT book_id FROM books WHERE book_number = %s", [book_number])
            if cursor.fetchone():
                return JsonResponse({"message": "Book number already exists"}, status=400)

            # Author exists?
            cursor.execute("SELECT author_id FROM author WHERE author_name = %s", [author_name])
            author = cursor.fetchone()
            if author:
                author_id = author[0]
            else:
                cursor.execute(
                    "INSERT INTO author (author_name) VALUES (%s) RETURNING author_id", [author_name]
                )
                author_id = cursor.fetchone()[0]

            # Insert book
            cursor.execute(
                """
                INSERT INTO books (title, total_copies, available_copies, author_id, book_number)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [title, total_copies, total_copies, author_id, book_number]
            )

        return JsonResponse({"message": "Book added successfully!"})

    return JsonResponse({"message": "Invalid request"}, status=400)


@csrf_exempt
def search_book(request):
    if request.method == "GET":
        book_number = request.GET.get("book_number")
        if not book_number:
            return JsonResponse({"message": "Book number required"}, status=400)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT b.title, a.author_name, b.book_number, b.available_copies
                FROM books b
                LEFT JOIN author a ON b.author_id = a.author_id
                WHERE b.book_number = %s
                """,
                [book_number]
            )
            rows = cursor.fetchall()

        books = [
            {"title": row[0], "author": row[1], "book_number": row[2], "available": row[3]}
            for row in rows
        ]

        return JsonResponse({"status": "success", "books": books})

    return JsonResponse({"status": "fail", "message": "Invalid request"}, status=400)


# ================== STUDENT MANAGEMENT ==================
@csrf_exempt
def add_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        roll_no = data.get("roll_no")
        batch = data.get("batch")
        faculty = data.get("faculty")
        email = data.get("email")

        if not name or not roll_no:
            return JsonResponse({"message": "Name and Roll No required"}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM users WHERE roll_no = %s", [roll_no])
            if cursor.fetchone():
                return JsonResponse({"message": "Roll number already exists"}, status=400)

            cursor.execute(
                "INSERT INTO users (name, roll_no, batch, faculty, email) VALUES (%s,%s,%s,%s,%s)",
                [name, roll_no, batch, faculty, email]
            )

        return JsonResponse({"message": "Student added successfully!"})

    return JsonResponse({"message": "Invalid request"}, status=400)


@csrf_exempt
def search_student(request):
    if request.method == "GET":
        roll_no = request.GET.get("roll_no")
        if not roll_no:
            return JsonResponse({"message": "Roll No required"}, status=400)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name, roll_no, batch, faculty, email FROM users WHERE roll_no = %s", [roll_no]
            )
            row = cursor.fetchone()

        if row:
            student = {"name": row[0], "roll_no": row[1], "batch": row[2], "faculty": row[3], "email": row[4]}
            return JsonResponse({"status": "success", "student": student})
        else:
            return JsonResponse({"status": "fail", "message": "Student not found"}, status=404)

    return JsonResponse({"message": "Invalid request"}, status=400)


@csrf_exempt
def remove_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        roll_no = data.get("roll_no")
        if not roll_no:
            return JsonResponse({"message": "Roll Number required"}, status=400)

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Get student
                    cursor.execute("SELECT user_id FROM users WHERE roll_no=%s", [roll_no])
                    student = cursor.fetchone()
                    if not student:
                        return JsonResponse({"message": "Student not found"}, status=404)

                    user_id = student[0]

                    # Check if any book still issued
                    cursor.execute(
                        "SELECT COUNT(*) FROM issued_book WHERE user_id=%s AND status='issued'", [user_id]
                    )
                    count = cursor.fetchone()[0]
                    if count > 0:
                        return JsonResponse({"message": f"Cannot delete student: {count} book(s) still issued."}, status=400)

                    # Optional: remove returned book records
                    cursor.execute("DELETE FROM issued_book WHERE user_id=%s AND status='returned'", [user_id])

                    # Delete student
                    cursor.execute("DELETE FROM users WHERE user_id=%s", [user_id])

            return JsonResponse({"message": f"Student {roll_no} removed successfully!"})

        except Exception as e:
            return JsonResponse({"message": f"Database error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid request"}, status=400)


# ================== ISSUE / RETURN BOOK ==================
@csrf_exempt
def issue_book(request):
    if request.method == "POST":
        data = json.loads(request.body)
        roll_no = data.get("roll_no")
        book_number = data.get("book_number")
        issue_date = data.get("issue_date")
        return_date = data.get("return_date")

        if not roll_no or not book_number or not issue_date or not return_date:
            return JsonResponse({"message": "All fields are required"}, status=400)

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Student ID
                    cursor.execute("SELECT user_id FROM users WHERE roll_no = %s", [roll_no])
                    student = cursor.fetchone()
                    if not student:
                        return JsonResponse({"message": "Student not found"}, status=404)

                    # Book ID
                    cursor.execute("SELECT book_id, available_copies FROM books WHERE book_number = %s", [book_number])
                    book = cursor.fetchone()
                    if not book:
                        return JsonResponse({"message": "Book not found"}, status=404)
                    if book[1] <= 0:
                        return JsonResponse({"message": "No available copies"}, status=400)

                    # Insert issued_book
                    cursor.execute(
                        "INSERT INTO issued_book (issue_date, return_date, status, user_id, book_id) VALUES (%s,%s,%s,%s,%s)",
                        [issue_date, return_date, "issued", student[0], book[0]]
                    )

                    # Decrease available copies
                    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s", [book[0]])

            return JsonResponse({"message": f"Book {book_number} issued to {roll_no} successfully!"})

        except Exception as e:
            return JsonResponse({"message": f"Database error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid request"}, status=400)


@csrf_exempt
def return_book(request):
    if request.method == "POST":
        data = json.loads(request.body)
        roll_no = data.get("roll_no")
        book_number = data.get("book_number")
        return_date = data.get("return_date")  # optional

        if not roll_no or not book_number:
            return JsonResponse({"message": "Roll Number and Book Number required"}, status=400)

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Student ID
                    cursor.execute("SELECT user_id FROM users WHERE roll_no=%s", [roll_no])
                    student = cursor.fetchone()
                    if not student:
                        return JsonResponse({"message": "Student not found"}, status=404)

                    # Book ID
                    cursor.execute("SELECT book_id FROM books WHERE book_number=%s", [book_number])
                    book = cursor.fetchone()
                    if not book:
                        return JsonResponse({"message": "Book not found"}, status=404)

                    # Check issued
                    cursor.execute(
                        "SELECT issue_id FROM issued_book WHERE user_id=%s AND book_id=%s AND status='issued'",
                        [student[0], book[0]]
                    )
                    issued = cursor.fetchone()
                    if not issued:
                        return JsonResponse({"message": "This book was not issued to this student"}, status=400)

                    # Update status
                    cursor.execute(
                        "UPDATE issued_book SET status='returned', return_date=%s WHERE issue_id=%s",
                        [return_date or 'NOW()', issued[0]]
                    )

                    # Increase available copies
                    cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_id=%s", [book[0]])

            return JsonResponse({"message": f"Book {book_number} returned by {roll_no} successfully!"})

        except Exception as e:
            return JsonResponse({"message": f"Database error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid request"}, status=400)


# ================== DASHBOARD STATS ==================
@csrf_exempt
def dashboard_stats(request):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            total_students = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(total_copies) FROM books")
            total_books = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM issued_book WHERE status='issued'")
            total_issued = cursor.fetchone()[0]

        return JsonResponse({
            "total_students": total_students,
            "total_books": total_books,
            "total_issued": total_issued
        })

    return JsonResponse({"message": "Invalid request"}, status=400)