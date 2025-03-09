import os
import tempfile
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import json
from .calculations import calculate_distributions

def grade_calculator(request):
    if request.method == "POST":
        # รับค่าข้อมูลจากฟอร์ม
        current_credits = float(request.POST.get("current_credits", 0) or 0)
        current_gpa = float(request.POST.get("current_gpa", 0) or 0)
        target_gpa = float(request.POST.get("target_gpa", 0) or 0)
        courses_1_credit = max(0, int(request.POST.get("courses_1_credit", 0) or 0))
        courses_2_credits = max(0, int(request.POST.get("courses_2_credits", 0) or 0))
        courses_3_credits = max(0, int(request.POST.get("courses_3_credits", 0) or 0))
        courses_4_credits = max(0, int(request.POST.get("courses_4_credits", 0) or 0))
        courses_5_credits = max(0, int(request.POST.get("courses_5_credits", 0) or 0))
        courses_6_credits = max(0, int(request.POST.get("courses_6_credits", 0) or 0))

        # คำนวณหน่วยกิตที่เหลือ
        remaining_credits = (
            courses_1_credit
            + 2 * courses_2_credits
            + 3 * courses_3_credits
            + 4 * courses_4_credits
            + 5 * courses_5_credits
            + 6 * courses_6_credits
        )

        if remaining_credits == 0:
            return JsonResponse({"result": "กรุณากรอกข้อมูลหน่วยกิตที่เหลือให้ถูกต้อง"})

        # คำนวณเกรดที่ต้องการ
        total_credits = current_credits + remaining_credits
        required_grade = (
            (target_gpa * total_credits) - (current_gpa * current_credits)
        ) / remaining_credits

        if required_grade > 4:
            return JsonResponse({"result": "ไม่สามารถทำได้เนื่องจากต้องการเกรดมากกว่า 4.00"})
        elif required_grade < 0:
            return JsonResponse({"result": "ไม่สามารถทำได้เนื่องจากต้องการเกรดน้อยกว่า 0"})

        # เตรียมข้อมูลหน่วยกิต
        courses = [
            (6, courses_6_credits),
            (5, courses_5_credits),
            (4, courses_4_credits),
            (3, courses_3_credits),
            (2, courses_2_credits),
            (1, courses_1_credit),
        ]
        courses = [(credit, count) for credit, count in courses if count > 0]

        # คำนวณแผนการกระจายเกรด
        distributions = calculate_distributions(courses, required_grade, remaining_credits)
    
        

        # ส่งผลลัพธ์กลับ
        result = f"คุณต้องทำเกรดเฉลี่ยอย่างน้อย {required_grade:.2f} ในวิชาที่เหลือ ({remaining_credits} หน่วยกิต) เพื่อให้ได้ GPA {target_gpa:.2f} หรือมากกว่า"
        return JsonResponse({"result": result, "distributions": distributions})

    return render(request, "app_plan/home.html")

def export_pdf(request):
    if request.method == "POST":
        # ✅ ดึงข้อมูลจากฟอร์ม
        current_credits = float(request.POST.get("current_credits", 0) or 0)
        current_gpa = float(request.POST.get("current_gpa", 0) or 0)
        target_gpa = float(request.POST.get("target_gpa", 0) or 0)
        courses_1_credit = max(0, int(request.POST.get("courses_1_credit", 0) or 0))
        courses_2_credits = max(0, int(request.POST.get("courses_2_credits", 0) or 0))
        courses_3_credits = max(0, int(request.POST.get("courses_3_credits", 0) or 0))
        courses_4_credits = max(0, int(request.POST.get("courses_4_credits", 0) or 0))
        courses_5_credits = max(0, int(request.POST.get("courses_5_credits", 0) or 0))
        courses_6_credits = max(0, int(request.POST.get("courses_6_credits", 0) or 0))

        remaining_credits = (
            courses_1_credit
            + 2 * courses_2_credits
            + 3 * courses_3_credits
            + 4 * courses_4_credits
            + 5 * courses_5_credits
            + 6 * courses_6_credits
        )

        if remaining_credits == 0:
            return JsonResponse({"error": "กรุณากรอกข้อมูลหน่วยกิตที่เหลือให้ถูกต้อง"})

        total_credits = current_credits + remaining_credits
        required_grade = ((target_gpa * total_credits) - (current_gpa * current_credits)) / remaining_credits

        courses = [(6, courses_6_credits), (5, courses_5_credits), (4, courses_4_credits), (3, courses_3_credits),
                   (2, courses_2_credits), (1, courses_1_credit)]
        courses = [(credit, count) for credit, count in courses if count > 0]

        distributions = calculate_distributions(courses, required_grade, remaining_credits)

        result = f"คุณต้องทำเกรดเฉลี่ยอย่างน้อย {required_grade:.2f} ในวิชาที่เหลือ ({remaining_credits} หน่วยกิต) เพื่อให้ได้ GPA {target_gpa:.2f} หรือมากกว่า"

        # ✅ ใช้ไฟล์ PDF ชั่วคราว
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf_path = temp_pdf.name

        try:
            doc = SimpleDocTemplate(temp_pdf_path, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            # ✅ หัวเรื่อง
            elements.append(Paragraph("<b>Grade Calculation Report</b>", styles["Title"]))
            elements.append(Spacer(1, 12))

            # ✅ ตารางข้อมูลหลัก
            data = [
                ["Current Credits:", current_credits],
                ["Current GPA:", current_gpa],
                ["Target GPA:", target_gpa],
                ["Remaining Credits:", remaining_credits],
                ["Required Grade:", required_grade],
            ]
            table = Table(data, colWidths=[150, 150])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

            # ✅ แสดงแผนการกระจายเกรด
            for idx, distribution in enumerate(distributions):
                elements.append(Paragraph(f"<b>Plan {idx + 1}: Required GPA: {distribution['avgGrade']:.2f}</b>", styles["Heading2"]))
                elements.append(Spacer(1, 6))

                table_data = [["Credit", "Subjects", "Grade Needed"]]
                for credit, details in distribution.items():
                    if isinstance(details, dict):
                        for grade, count in details.items():
                            if count > 0:
                                table_data.append([f"{credit}-credit", f"{count} subjects", f"Grade {grade}"])

                plan_table = Table(table_data, colWidths=[100, 100, 150])
                plan_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]))

                elements.append(plan_table)
                elements.append(Spacer(1, 12))  # ระยะห่างแต่ละแผน

            # ✅ บันทึก PDF ลงไฟล์ชั่วคราว
            doc.build(elements)

            # ✅ ส่ง PDF กลับไปให้ผู้ใช้
            with open(temp_pdf_path, "rb") as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="grade_plan.pdf"'

        finally:
            # ✅ ลบไฟล์ PDF ชั่วคราวเมื่อสร้างเสร็จ
            os.remove(temp_pdf_path)

        return response

    return JsonResponse({"error": "Method not allowed"}, status=405)