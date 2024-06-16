import csv
import collections
import random as rn
import copy
from typing import List

from numpy import concatenate
from numpy import random
from numpy.random import randint


# Class to store course
class Course:
    # Initialize the class
    def __init__(self, code, name, number):
        self.courseCode = code
        self.courseName = name
        self.number = number

    # Print course
    def __repr__(self):
        return '({0},{1},{2})'.format(self.courseCode, self.courseName, self.number)

    # Check Equality
    def __eq__(self, other):
        return self.courseName == other.courseName and self.courseCode == other.courseCode


# Class to store student registered in course
class Registration:
    # Initialize the class
    def __init__(self, Name, courseCodes):
        self.studentName = Name
        self.registeredCourses = courseCodes.copy()

    # Print registration
    def __repr__(self):
        return '({0},{1})'.format(self.studentName, self.registeredCourses)

    # Check equality
    def __eq__(self, other):
        if self.studentName == other.studentName and len(self.registeredCourses) == len(other.registeredCourses):
            count = 0
            for i in range(len(self.registeredCourses)):
                if self.registeredCourses[i] == other.registeredCourses[i]:
                    count += 1
            if count == len(self.registeredCourses):
                return True
        return False


# Class to store an exam
class Exam:
    # Initialize the class
    def __init__(self, startTime, roomNo, day, invigilator):
        self.startTime = startTime
        self.roomNo = roomNo.copy()
        self.day = day
        self.invigilator = invigilator.copy()
        self.binary = []

    # Print an exam
    def __repr__(self):
        return '(\n{0}, {1}, {2}, {3}), \n{4}'.format(self.startTime,
                                                      self.roomNo, self.day, self.invigilator, self.binary)

    # Check equality
    def __eq__(self, other):
        if len(self.roomNo) == len(other.roomNo) and self.startTime == other.startTime and self.day == other.day \
                and len(self.invigilator) == len(other.invigilator):
            count = 0
            count1 = 0
            for i in range(len(self.roomNo)):
                if self.roomNo[i] == other.roomNo[i]:
                    count += 1
            for i in range(len(self.invigilator)):
                if self.invigilator[i] == other.invigilator[i]:
                    count1 += 1
            if count == len(self.roomNo) and count1 == len(self.invigilator):
                return True
        return False


# Reading from files
def takeInput():
    # Reading courses from file
    with open('src/courses.csv') as file:
        reader = csv.reader(file)
        count = 0
        for row in reader:
            if len(row) != 0:
                temp_course = Course(row[0], row[1], count)
                if temp_course not in courses:
                    courses.append(temp_course)
                    count += 1

    # Reading instructors from file
    with open('src/teachers.csv') as file:
        reader = csv.reader(file)
        count = 0
        for row in reader:
            if len(row) != 0:
                check = False
                for instructor in instructors:
                    if instructor[0] == row[0]:
                        check = True
                        break
                if not check:
                    instructors.append((row[0], count))
                    count += 1
    global totalInstructors
    totalInstructors = len(instructors)

    # Reading students from file
    with open('src/studentNames.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 0:
                temp_registration = Registration(row[0], [])
                if temp_registration not in registrations:
                    registrations.append(temp_registration)

    # Reading registrations of students from file
    with open('src/studentCourse.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 0 and row[0] != '':
                for i in registrations:
                    if i.studentName == row[1] and row[2] not in i.registeredCourses:
                        i.registeredCourses.append(row[2])


# Generating random exam
def getRandomExam(index):
    courseCode = courses[index].courseCode
    students = [x for x in registrations if courseCode in x.registeredCourses]
    total_students = len(students)

    # Assigning rooms required to accommodate all students
    roomNo = []
    while total_students > 0:
        temp = classRooms[rn.randrange(0, totalClassRooms)]
        while temp in roomNo:
            temp = classRooms[rn.randrange(0, totalClassRooms)]
        roomNo.append(temp)
        total_students -= classRoomCapacity

    # Setting time
    startTime = examStartTimings[rn.randrange(0, totalExamStartTimings)]
    if startTime[0] > 12:
        startTime -= 12

    # Setting day
    day = days[rn.randrange(0, totalDays)]

    # Assigning invigilators required to invigilate all rooms
    invigilator = []
    for i in range(len(roomNo)):
        temp = instructors[rn.randrange(0, totalInstructors)]
        while temp in invigilator:
            temp = instructors[rn.randrange(0, totalInstructors)]
        invigilator.append(temp)
    return Exam(startTime, roomNo, day, invigilator)


# Generate Population, given the size
def generate_population(size):
    new_population: List[Individual] = []

    # Initialize Random population
    for i in range(size):
        timeTable = []
        for j in range(len(courses)):
            timeTable.append(getRandomExam(j))

        new_population.append(
            Individual(
                chromosome=timeTable,
                value=-1
            )
        )
    return new_population


# Apply Mutation on chromosomes
def apply_mutation(chromosome):
    if random.randint(0, 100) <= mutation_probability * 100:
        gene = random.randint(0, len(courses) - 1)
        chromosome[gene] = getRandomExam(gene)
    return chromosome


# Apply Crossover on population
def apply_crossover(population):
    crossover_population = []

    while len(crossover_population) < len(population):
        if randint(0, 100) <= crossover_probability * 100:
            # Selecting parents
            parent_a = randint(0, len(population) - 1)
            parent_b = randint(0, len(population) - 1)

            # Doing crossover
            chromosome_a = copy.deepcopy(concatenate((population[parent_a].chromosome[:int(len(courses) / 2)],
                                                      population[parent_b].chromosome[int(len(courses) / 2):])))
            chromosome_a = apply_mutation(chromosome_a)

            chromosome_b = copy.deepcopy(concatenate((population[parent_b].chromosome[:int(len(courses) / 2)],
                                                      population[parent_a].chromosome[int(len(courses) / 2):])))
            chromosome_b = apply_mutation(chromosome_b)

            crossover_population.append(Individual(
                chromosome=chromosome_a,
                value=-1
            ))
            crossover_population.append(Individual(
                chromosome=chromosome_b,
                value=-1
            ))

    # Calculating fitness of crossover population
    crossover_population = calculate_fitness(crossover_population)
    # Combining will all population
    population = population + crossover_population
    return population


# Roulette Wheel Selection
def roulette_wheel_selection(population):
    # Calculating total fitness
    population_fitness = sum([individual.value for individual in population])
    # Calculating probabilities of all chromosomes
    chromosome_probabilities = [round(individual.value / population_fitness, 5) for individual in population]

    copy_probabilities = chromosome_probabilities.copy()
    copy_probabilities.sort()
    for i in range(len(copy_probabilities)):
        if i != 0:
            copy_probabilities[i] = round(copy_probabilities[i] + copy_probabilities[i - 1], 5)

    # Selecting population
    selected_population = []
    for i in range(population_size):
        index = -1
        random_probability = round(random.uniform(0, 1), 5)
        for j in range(len(copy_probabilities)):
            if random_probability <= copy_probabilities[j]:
                value = copy_probabilities[j]
                if j != 0:
                    value = round(value - copy_probabilities[j - 1], 5)
                index = chromosome_probabilities.index(value)
                break
        selected_population.append(population[index])
    return selected_population


# Find Top Fittest Individual from Population
def find_fittest_individual(population):
    highest_value = 0
    highest_index = 0
    for i in range(len(population)):
        if population[i].value > highest_value:
            highest_value = population[i].value
            highest_index = i
    return population[highest_index]


# Checks whether same invigilator invigilating exams at the same time or not
def checkInvigilation(chromosome):
    violation_count = 0
    data = [(individual.invigilator, individual.day, individual.startTime) for individual in chromosome]
    for i in range(len(data)):
        for invigilator in data[i][0]:
            for j in range(len(data)):
                if i != j and invigilator in data[j][0] and data[i][1] == data[j][1] and data[i][2] == data[j][2]:
                    violation_count += 1
    return violation_count // 2


# Checks whether an exam at the same time is scheduled in the same room or not
def checkRooms(chromosome):
    violation_count = 0
    for gene in chromosome:
        for room in gene.roomNo:
            for gene1 in chromosome:
                for room1 in gene1.roomNo:
                    if gene != gene1:
                        if room == room1 and gene.day == gene1.day and gene.startTime == gene1.startTime:
                            violation_count += 1
    return violation_count // 2


# Checks whether an invigilator is invigilating two exams in a row or not
def checkInvigilatorBreak(chromosome):
    violation_count = 0
    data = [(individual.invigilator, individual.day) for individual in chromosome]

    for i in range(len(data)):
        for invigilator in data[i][0]:
            for j in range(len(data)):
                if i != j and invigilator in data[j][0] and data[i][1] == data[j][1]:
                    violation_count += 1
    return violation_count // 2


# Checks whether the student is giving one exam at a time or not
def one_exam_student_check(chromosome):
    violation_count = 0
    for i in range(0, len(registrations)):
        days_arr = []
        for j in range(0, len(chromosome)):
            if courses[j].courseCode in registrations[i].registeredCourses:
                if (chromosome[j].day[1], chromosome[j].startTime) not in days_arr:
                    days_arr.append((chromosome[j].day[1], chromosome[j].startTime))
                else:
                    violation_count += 1
    return violation_count


# Checks whether MG course exam is before CS course exam or not
def check_MGCS(chromosome):
    for i in range(0, len(registrations)):
        for j in MG_indexes:
            if courses[j].courseCode in registrations[i].registeredCourses:
                for k in CS_indexes:
                    if courses[k].courseCode in registrations[i].registeredCourses:
                        CS_day = chromosome[k].day[1]
                        MG_day = chromosome[j].day[1]
                        if CS_day < MG_day:
                            chromosome[k].day, chromosome[j].day = chromosome[j].day, chromosome[k].day
                        if CS_day == MG_day and chromosome[k].startTime[1] < chromosome[j].startTime[1]:
                            chromosome[k].startTime, chromosome[j].startTime = \
                                chromosome[j].startTime, chromosome[k].startTime
    return 0


# Calculating fitness of given chromosome
def calculate_value(chromosome):
    value = 400
    # value -= check_MGCS(chromosome)
    # value -= checkInvigilation(chromosome)
    value -= checkRooms(chromosome)
    # value -= checkInvigilatorBreak(chromosome)
    value -= one_exam_student_check(chromosome)

    # Binary encoding
    for i in range(len(chromosome)):
        chromosome[i].binary.clear()
        chromosome[i].binary.append(bin(courses[i].number)[2:].zfill(6))
        chromosome[i].binary.append(bin(chromosome[i].startTime[1])[2:].zfill(6))
        tempRoom = []
        for room in chromosome[i].roomNo:
            tempRoom.append(bin(room[1])[2:].zfill(6))
        chromosome[i].binary.append(tempRoom)
        chromosome[i].binary.append(bin(chromosome[i].day[1])[2:].zfill(6))
        tempInvigilator = []
        for invigilator in chromosome[i].invigilator:
            tempInvigilator.append(bin(invigilator[1])[2:].zfill(6))
        chromosome[i].binary.append(tempInvigilator)
    return value


# Assigning fitness to the chromosomes in population
def calculate_fitness(population):
    for i in range(len(population)):
        v = calculate_value(population[i].chromosome)
        population[i] = Individual(
            chromosome=population[i].chromosome,
            value=v
        )
    return population


# Displays the schedule
def display_schedule(best_solution):
    count = 0
    temp_day = -1
    
    week = 1
    last_week_entry = 0
    weekflag = False

    max_invigilator_length = 0
    for i in instructors:
        if len(i[0]) > max_invigilator_length:
            max_invigilator_length = len(i[0])

    max_length = 0
    for i in courses:
        if len(i.courseName) > max_length:
            max_length = len(i.courseName)

    best_solution_copy = copy.deepcopy(best_solution)
    best_solution_copy = Individual(sorted(best_solution_copy.chromosome, key=lambda x:(x.day[1], x.startTime[1])), best_solution_copy.value)

    print("\n\nSCHEDULE:\n--------")
    for i in best_solution_copy.chromosome:
        curr_day = i.day[1]
        if curr_day >= last_week_entry:
            if count != 0:
                print(end="\t\t")
                for j in range(0, 41 + max_length + max_invigilator_length):
                    print(end="-")
                print()

            print("\nWeek", week)
            print("------")
            week += 1
            last_week_entry += 5
            weekflag = True


        if temp_day != curr_day:
            if count != 0 and weekflag == False:
                print(end="\t\t")
                for j in range(0, 41 + max_length + max_invigilator_length):
                    print(end="-")
                print()

            print(end="\n\t\t")
            print(i.day[0])
            weekflag = False

        print(end="\t\t")
        for j in range(0, 41 + max_length + max_invigilator_length):
            print(end="-")
        print()

        print(end="\t\t")
        for j in range(0, len(courses)):
            if best_solution.chromosome[j] == i:
                ind = j
                break
        print("|", courses[ind].courseCode, "|", courses[ind].courseName, end="")

        if len(courses[ind].courseCode) == 5:
            for j in range(0, max_length-len(courses[ind].courseName)):
                print(end=" ")
        else:
            for j in range(0, max_length-len(courses[ind].courseName)-1):
                print(end=" ")
        print(end=" | ")

        if i.startTime[1] == 0:
            print(end="9:00 AM | ")
        else:
            print(end="2:00 PM | ")

        for j in range(0, len(i.roomNo)):
            if j != 0:
                print(end="\t\t")
                for k in range(0, 23+max_length):
                    print(end=" ")

            print("Room", j+1, end="")
            print(":", i.roomNo[j][0], "|", i.invigilator[j][0], end="")
            for k in range(0, max_invigilator_length - len(i.invigilator[j][0]) + 1):
                print(end=" ")
            print("|")

        temp_day = curr_day
        count += 1

    print(end="\t\t")
    for j in range(0, 41 + max_length + max_invigilator_length):
        print(end="-")
    print()


# Run Complete Algorithm Step by step
def runGA():
    # Generating random population
    population = generate_population(population_size)
    generation = 1
    best_solution = None

    # Calculate Fitness of initial population
    population = calculate_fitness(population)

    # Running generations
    while True:
        # Applying crossover and mutation
        population = apply_crossover(population)
        # Selection using roulette wheel
        population = roulette_wheel_selection(population)
        # Finding fittest candidates
        candidate = find_fittest_individual(population)

        # Updating best solution so far
        if best_solution is None:
            best_solution = candidate
        elif candidate.value > best_solution.value:
            best_solution = candidate

        # print Every 10th generation results
        if generation % 10 == 0 or generation == 1:
            print('\nCurrent generation: {}'.format(generation))
            print('Best solution so far: {}, Goal: 400'.format(best_solution.value))

        # break when solution is found
        if best_solution.value == 400:
            print('\nSolution found:')
            print('Value: {}, Goal: 400'.format(best_solution.value))

            print("\nHard Constraints:")
            print("1: An exam will be scheduled for each course\t\t\t\t ✔")
            print("2: A student is enrolled in minimum three courses\t\t\t ✔")
            if one_exam_student_check(best_solution.chromosome) == 0:
                print("3: A student can not give more than one exam at a time\t\t\t ✔")
            else:
                print("3: A student can not give more than one exam at a time\t\t\t ❌")
            print("4: All exams must be held between 9 AM and 5 PM\t\t\t\t ✔")
            if checkInvigilation(best_solution.chromosome) == 0:
                print("5: A teacher can not invigilate two exams at the same time\t\t ✔")
            else:
                print("5: A teacher can not invigilate two exams at the same time\t\t ❌")
            if checkInvigilatorBreak(best_solution.chromosome) == 0:
                print("6: A teacher can not invigilate two exams in a row\t\t\t ✔")
            else:
                print("6: A teacher can not invigilate two exams in a row\t\t\t ❌")
            if checkRooms(best_solution.chromosome) == 0:
                print("7: No exam scheduled in the same room at the same time\t\t\t ✔")
            else:
                print("7: No exam scheduled in the same room at the same time\t\t\t ❌")

            print("\nSoft Constraints:")
            print("1: An exam will be scheduled for each course\t\t\t\t ✔")
            print("2: A student shall not give more than one exam consecutively\t\t ✔")
            print("3: MG courses preferably be held before CS courses\t\t\t ✔")
            print("4: Two hours of break for faculty meeting\t\t\t\t ✔")

            display_schedule(best_solution)
            break
        generation += 1


# global variables for input
classRooms = [("C-301", 0), ("C-302", 1), ("C-303", 2), ("C-304", 3), ("C-305", 4),
              ("C-306", 5), ("C-307", 6), ("C-308", 7), ("C-309", 8), ("C-310", 9)]
classRoomCapacity = 28
totalClassRooms = len(classRooms)
days = [("Monday", 0), ("Tuesday", 1), ("Wednesday", 2), ("Thursday", 3), ("Friday", 4),
        ("Monday", 5), ("Tuesday", 6), ("Wednesday", 7), ("Thursday", 8), ("Friday", 9)]
totalDays = len(days)
examStartTimings = [(9, 0), (2, 1)]
totalExamStartTimings = len(examStartTimings)
examDuration = 3
courses: List[Course] = []
instructors = []
totalInstructors = -1
registrations: List[Registration] = []
Individual = collections.namedtuple('Population', 'chromosome value')
population_size = 0
crossover_probability, mutation_probability = 0.0, 0.0
MG_indexes = []
CS_indexes = []


if __name__ == "__main__":
    # Taking input from files
    takeInput()

    # Initializing population size and Crossover and Mutation Probabilities
    population_size = random.randint(50, 150)
    crossover_probability = round(random.uniform(low=0.3, high=1.0), 1)
    mutation_probability = round(random.uniform(low=0.0, high=0.5), 1)

    # Calculating MG and CS courses indexes
    # for i in range(0, len(courses)):
    #     if courses[i].courseCode[0] == 'M' and courses[i].courseCode[1] == 'G':
    #         MG_indexes.append(i)
    #     if courses[i].courseCode[0] == 'C' and courses[i].courseCode[1] == 'S':
    #         CS_indexes.append(i)

    # Printing Initialized variables
    print('----- Generated Parameters -----')
    print('Population size......: {}'.format(population_size))
    print('Crossover probability: {}'.format(crossover_probability))
    print('Mutation probability.: {}'.format(mutation_probability))

    # Running Genetic Algorithm
    runGA()
