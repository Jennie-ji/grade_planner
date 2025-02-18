from django.shortcuts import render
from django.http import JsonResponse
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
