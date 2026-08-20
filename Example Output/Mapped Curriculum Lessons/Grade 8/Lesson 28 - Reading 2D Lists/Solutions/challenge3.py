timetable = [["Maths", 12], ["Music", 4], ["Science", 8]]
row = int(input("Lesson row 0 to 2: "))
print("Selected:", timetable[row][0], "in room", timetable[row][1])
print("Subjects:")
for lesson in timetable:
    print(lesson[0])
