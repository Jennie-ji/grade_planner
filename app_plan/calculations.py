grade_values = {"A": 4, "B+": 3.5, "B": 3, "C+": 2.5, "C": 2,
    "D+": 1.5, "D": 1, "F": 0}

def calculate_distributions(courses, required_grade, remaining_credits):
    """
    คำนวณแผนการกระจายเกรดสำหรับวิชาที่เหลือ
    """
    distributions = []

    def recursive_calculate(plan, total_score, level):
        if level == len(courses):
            avg_grade = total_score / remaining_credits
            if avg_grade >= required_grade:
                clean_plan = {
                    credit: grades
                    for credit, grades in plan.items()
                    if sum(grades.values()) > 0
                }
                distributions.append({"avgGrade": round(avg_grade, 2), **clean_plan})
            return

        credit, max_count = courses[level]
        for iA in range(max_count + 1):
            for iBp in range(max_count - iA + 1):
                for iB in range(max_count - iA - iBp + 1):
                    for iCp in range(max_count - iA - iBp - iB + 1):
                        for iC in range(max_count - iA - iBp - iB - iCp + 1):
                            for iDp in range(max_count - iA - iBp - iB - iCp - iC + 1):
                                for iD in range(max_count - iA - iBp - iB - iCp - iC - iDp + 1):
                                    iF = max_count - iA - iBp - iB - iCp - iC - iDp - iD
                                    if iF < 0:
                                        continue

                                    new_plan = plan.copy()
                                    new_plan[credit] = {
                                        "A": iA, "B+": iBp, "B": iB,
                                        "C+": iCp, "C": iC, "D+": iDp,
                                        "D": iD, "F": iF
                                    }
                                    total_score_for_credit = (
                                        grade_values["A"] * iA +
                                        grade_values["B+"] * iBp +
                                        grade_values["B"] * iB +
                                        grade_values["C+"] * iCp +
                                        grade_values["C"] * iC +
                                        grade_values["D+"] * iDp +
                                        grade_values["D"] * iD +
                                        grade_values["F"] * iF
                                    ) * credit
                                    recursive_calculate(new_plan, total_score + total_score_for_credit, level + 1)


    recursive_calculate({}, 0, 0)
    return distributions[:10]  # จำกัดไม่เกิน 10 แผน
