def merge_intervals(times):
    intervals = []
    i = 0
    while i < len(times):
        start = times[i]
        end = times[i + 1]
        intervals.append((start, end))
        i += 2

    intervals.sort()

    merged = []
    for current in intervals:
        if len(merged) == 0:
            merged.append(current)
        else:
            last = merged[-1]
            if last[1] < current[0]:
                merged.append(current)
            else:
                merged[-1] = (last[0], max(last[1], current[1]))
    return merged


def intersect_intervals(a, b):
    result = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        a_start = a[i][0]
        a_end = a[i][1]
        b_start = b[j][0]
        b_end = b[j][1]

        start = max(a_start, b_start)
        end = min(a_end, b_end)

        if start < end:
            result.append((start, end))

        if a_end < b_end:
            i += 1
        else:
            j += 1
    return result


def appearance(intervals):
    lesson_start = intervals['lesson'][0]
    lesson_end = intervals['lesson'][1]
    lesson = [(lesson_start, lesson_end)]

    pupil = merge_intervals(intervals['pupil'])
    tutor = merge_intervals(intervals['tutor'])

    temp = intersect_intervals(pupil, lesson)
    both = intersect_intervals(temp, tutor)

    total = 0
    for pair in both:
        start = pair[0]
        end = pair[1]
        total += end - start

    return total


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },

    {
        'intervals': {
            'lesson': [1600000000, 1600003600],
            'pupil': [1600000000, 1600003600],
            'tutor': [1600000000, 1600003600]
        },
        'answer': 3600
    },

    {
        'intervals': {
            'lesson': [1600000000, 1600003600],
            'pupil': [1600000000, 1600003600],
            'tutor': [1600001800, 1600003000]
        },
        'answer': 1200
    },

    {
        'intervals': {
            'lesson': [1600000000, 1600003600],
            'pupil': [1599990000, 1599993600],
            'tutor': [1600003700, 1600004000]
        },
        'answer': 0
    },

    {
        'intervals': {
            'lesson': [1600000000, 1600003600],
            'pupil': [1600000100, 1600000150, 1600000200, 1600000300, 1600000500, 1600001000],
            'tutor': [1600000000, 1600003600]
        },
        'answer': 650
    },

    {
        'intervals': {
            'lesson': [1600000000, 1600003600],
            'pupil': [1600001000, 1600002000],
            'tutor': [1600001200, 1600001800]
        },
        'answer': 600
    }
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
