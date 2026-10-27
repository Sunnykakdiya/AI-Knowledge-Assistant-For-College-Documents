
import fitz
from pathlib import Path

output_path = Path("data/documents/sample_college_policy.pdf")
output_path.parent.mkdir(parents=True, exist_ok=True)

pages = [
    """Sample College Handbook

Attendance Policy

Students should maintain at least 75 percent attendance
in each course to be eligible for regular semester
examinations. Students should contact the academic
office if they have questions about attendance records.""",

    """Examination Policy

Students must carry their college identity card during
examinations. The examination timetable is published
by the examination department. Students should check
official college notices for schedule changes.""",

    """Library Policy

Students may borrow library books using their college
identity card. Books should be returned by the due date.
Students should contact library staff to renew a book
or ask about borrowing rules."""
]

document = fitz.open()

for page_text in pages:
    page = document.new_page()
    page.insert_textbox(
        fitz.Rect(50, 50, 545, 750),
        page_text,
        fontsize=12,
    )

document.save(output_path)
document.close()

print(f"Sample PDF created: {output_path}")
