// ================= BASIC ELEMENTS =================
const loginSection = document.getElementById("login-section");
const app = document.getElementById("app");
const sections = document.querySelectorAll(".section");
const loginBtn = document.querySelector(".btn-primary");

// Dashboard elements
const totalBooks = document.getElementById("totalBooks");
const totalStudents = document.getElementById("totalStudents");
const totalIssued = document.getElementById("totalIssued");

// Book elements
const bookNumber = document.getElementById("bookNumber");
const bookTitle = document.getElementById("bookTitle");
const bookAuthor = document.getElementById("bookAuthor");
const totalCopies = document.getElementById("totalCopies");
const bookSearchNo = document.getElementById("bookSearchNo");

// Student elements
const studentName = document.getElementById("studentName");
const studentRoll = document.getElementById("studentRoll");
const studentBatch = document.getElementById("studentBatch");
const studentFaculty = document.getElementById("studentFaculty");
const studentEmail = document.getElementById("studentEmail");
const studentSearchRoll = document.getElementById("studentSearchRoll");
const studentSearchResult = document.getElementById("studentSearchResult");
const selectedStudentRoll = document.getElementById("selectedStudentRoll");
const removeStudentBtn = document.querySelector(".btn-danger");

// Issue/Return elements
const issueRollNo = document.getElementById("issueRollNo");
const issueBookNo = document.getElementById("issueBookNo");
const issueDateInput = document.getElementById("issueDate");
const returnDateInput = document.getElementById("ReturnDate"); // ID matches HTML
const issueBtn = document.getElementById("issueBtn");
const returnBtn = document.getElementById("returnBtn");

// ================= GLOBAL MESSAGE FUNCTION =================
function showMessage(elementId, message, type = "success") {
    const box = document.getElementById(elementId);
    box.innerText = message;
    box.className = `form-message ${type}`;
    box.style.display = "block";

    setTimeout(() => {
        box.style.display = "none";
    }, 3000);
}

// ================= LOGIN =================
loginBtn.addEventListener("click", async () => {
    const email = document.querySelector("#login-section input[type='text']").value;
    const password = document.querySelector("#login-section input[type='password']").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/api/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage("loginMessage", "Login successful", "success");
            setTimeout(() => {
                loginSection.style.display = "none";
                app.style.display = "flex";
                showSection("dashboard");
            }, 800);
        } else {
            showMessage("loginMessage", data.message, "error");
        }
    } catch (err) {
        showMessage("loginMessage", "Backend server not running", "error");
        console.error(err);
    }
});

// ================= LOGOUT =================
function logout() {
    app.style.display = "none";
    loginSection.style.display = "flex";
    document.querySelector("#login-section input[type='text']").value = "";
    document.querySelector("#login-section input[type='password']").value = "";
}

// ================= SHOW SECTION =================
function showSection(sectionId) {
    sections.forEach(section => section.style.display = "none");
    document.getElementById(sectionId).style.display = "block";

    if (sectionId === "dashboard") {
        loadDashboardStats();
    }
}

// ================= ADD BOOK =================
document.getElementById("addBookBtn").addEventListener("click", async () => {
    if (!bookNumber.value || !bookTitle.value || !bookAuthor.value || !totalCopies.value) {
        return showMessage("bookMessage", "All fields required", "error");
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/add-book/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                book_number: bookNumber.value,
                title: bookTitle.value,
                author: bookAuthor.value,
                total_copies: totalCopies.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage("bookMessage", data.message, "success");
            bookNumber.value = "";
            bookTitle.value = "";
            bookAuthor.value = "";
            totalCopies.value = "";
        } else {
            showMessage("bookMessage", data.message, "error");
        }
    } catch (err) {
        showMessage("bookMessage", "Server not running", "error");
        console.error(err);
    }
});

// ================= SEARCH BOOK =================
document.getElementById("bookSearchBtn").addEventListener("click", async () => {
    const bookNo = bookSearchNo.value.trim();
    if (!bookNo) return showMessage("bookMessage", "Enter book number", "error");

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/search-book/?book_number=${bookNo}`);
        const data = await response.json();

        const resultBox = document.getElementById("bookSearchResult");

        if (response.ok && data.books.length > 0) {
            const book = data.books[0];
            resultBox.style.display = "block";
            document.getElementById("resultBookTitle").innerText = book.title;
            document.getElementById("resultBookAuthor").innerText = book.author;
            document.getElementById("resultBookNo").innerText = book.book_number;
            document.getElementById("resultBookAvailable").innerText = book.available;
        } else {
            resultBox.style.display = "none";
            showMessage("bookMessage", "Book not found", "error");
        }
    } catch (err) {
        showMessage("bookMessage", "Server not running", "error");
        console.error(err);
    }
});

// ================= ADD STUDENT =================
document.getElementById("addStudentBtn").addEventListener("click", async () => {
    if (!studentName.value || !studentRoll.value || !studentEmail.value) {
        return showMessage("studentMessage", "Name, Roll & Email required", "error");
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/add-student/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: studentName.value,
                roll_no: studentRoll.value,
                batch: studentBatch.value,
                faculty: studentFaculty.value,
                email: studentEmail.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage("studentMessage", data.message, "success");
            document.querySelectorAll("#students input").forEach(i => i.value = "");
        } else {
            showMessage("studentMessage", data.message, "error");
        }
    } catch (err) {
        showMessage("studentMessage", "Server not running", "error");
        console.error(err);
    }
});

// ================= SEARCH STUDENT =================
document.getElementById("studentSearchBtn").addEventListener("click", async () => {
    const roll = studentSearchRoll.value.trim();
    if (!roll) return showMessage("studentSearchMessage", "Enter Roll No", "error");

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/search-student/?roll_no=${roll}`);
        const data = await response.json();

        if (data.status === "success") {
            studentSearchResult.style.display = "block";
            document.getElementById("resultName").innerText = data.student.name;
            document.getElementById("resultRoll").innerText = data.student.roll_no;
            document.getElementById("resultBatch").innerText = data.student.batch;
            document.getElementById("resultFaculty").innerText = data.student.faculty;
            document.getElementById("resultEmail").innerText = data.student.email;

            selectedStudentRoll.value = data.student.roll_no;
            removeStudentBtn.style.display = "inline-block";
        } else {
            studentSearchResult.style.display = "none";
            showMessage("studentMessage", data.message, "error");
        }
    } catch (err) {
        studentSearchResult.style.display = "none";
        showMessage("studentSearchMessage", "Server not running", "error");
        console.error(err);
    }
});
// ================= REMOVE STUDENT =================
removeStudentBtn.addEventListener("click", async () => {
    const roll = selectedStudentRoll.value;
    if (!roll) return showMessage("studentSearchMessage", "No student selected", "error");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/remove-student/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ roll_no: roll })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage("studentSearchMessage", data.message, "success");
            studentSearchResult.style.display = "none";
            studentSearchRoll.value = "";
        } else {
            showMessage("studentSearchMessage", data.message, "error");
        }
    } catch (err) {
        showMessage("studentSearchMessage", "Server not running", "error");
        console.error(err);
    }
});

// ================= ISSUE BOOK =================
issueBtn.addEventListener("click", async () => {
    const roll = issueRollNo.value.trim();
    const bookNo = issueBookNo.value.trim();
    const issueDateValue = issueDateInput.value;
    const returnDateValue = returnDateInput.value;

    if (!roll || !bookNo || !issueDateValue || !returnDateValue)
        return showMessage("issueMessage", "All fields required", "error");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/issue-book/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                roll_no: roll,
                book_number: bookNo,
                issue_date: issueDateValue,
                return_date: returnDateValue
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage("issueMessage", data.message, "success");
            issueRollNo.value = "";
            issueBookNo.value = "";
            issueDateInput.value = "";
            returnDateInput.value = "";
        } else {
            showMessage("issueMessage", data.message, "error");
        }
    } catch (err) {
        showMessage("issueMessage", "Server not running", "error");
        console.error(err);
    }
});

// ================= RETURN BOOK =================
returnBtn.addEventListener("click", async () => {
    const roll = issueRollNo.value.trim();
    const bookNo = issueBookNo.value.trim();

    if (!roll || !bookNo)
        return showMessage("issueMessage", "Enter Roll & Book No", "error");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/return-book/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ roll_no: roll, book_number: bookNo })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage("issueMessage", data.message, "success");
            issueRollNo.value = "";
            issueBookNo.value = "";
        } else {
            showMessage("issueMessage", data.message, "error");
        }
    } catch (err) {
        showMessage("issueMessage", "Server not running", "error");
        console.error(err);
    }
});

// ================= DASHBOARD =================
async function loadDashboardStats() {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/dashboard-stats/");
        const data = await response.json();

        totalStudents.innerText = data.total_students || 0;
        totalBooks.innerText = data.total_books || 0;
        totalIssued.innerText = data.total_issued || 0;
    } catch (err) {
        console.error("Dashboard load failed", err);
    }
}
