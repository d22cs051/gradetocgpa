
grades_conversion = {
    'A*': 10,
    'A': 10,
    'A-': 9,
    'B': 8,
    'B-': 7,
    'C': 6,
    'C-': 5,
    'D': 4,
    'E': 2,
    'F': 0
}


def convert(grade_map: dict = {}):
    # grade_map = {grade1(str): [fractles subs(int)], grade2(str): [fractles subs(int)]}
    total_score = 0
    total_fracs = 0
    for i in grade_map:
        for fracts in grade_map[i]:
            total_fracs += fracts
            total_score += fracts * grades_conversion[i]
            
    return {'total_score': total_score, 'total_fracs': total_fracs}


# grade map test
# print(convert({'B':[3,3],'B-':[3],'C':[2],'A-':[2,1]}))
