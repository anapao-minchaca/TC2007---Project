'''
Quantitative Methods and Simulation 
Project - Second Evaluation Term
Created April 26, 2022

@Authors:
- Emilio Alcántara Guzmán (A01027304)
- Ana Paola Minchaca García (A01026744)

'''

'''
    The user is first asked to write the input file he/she/them decides to review further upon.
    This input file is read, the 'c' is ignored because it signals a comment and the 
    clauses are counted until the end of the file so they can be appended into an array.
    We don't filter anything here so there is extra stuff that will be deleted later.
'''
import matplotlib.pyplot as plt
import random

fileName = input("Enter file name without the .txt: \n")
clauses = []
f = open(fileName+".txt", "r")
for lines in f:
    if(lines[0]== 'c'):
        continue
    elif(lines[0]=='%'):
        break
    else:
        clauses.append(lines)

'''
    We iterate through the clauses and get rid of extra things included in the instance, for example
    spaces, comments, words, and new lines. These clauses are then appended into a new array.
'''

temporalClause = []
aux = ''
for i in range(0,len(clauses)):
    for values in clauses[i]:
        if(values == " "):
            try:
                if(aux!="" and aux!=" "):
                    if(aux[0]=='0'):
                        aux = aux[1:len(aux)]
                        temporalClause.append(int(aux))
                    else:
                        temporalClause.append(int(aux))
                aux = '' 
            except:
                aux = ''
        elif(values == "p" or values=="c" or values=="n" or values=="f" or values == " " or values == "\n"):
            continue 
        else:
            aux += values

'''
    A new array is created where all the final clauses are included, these are separated into groups
    of 3 just like they appear in their respective file. Then, a random string is generated so we can
    have the initial values of all our variables. 
'''

variableClauses = temporalClause [2:len(temporalClause)]
allClauses = []

for generator in range(0,91):
    allClauses.append((variableClauses[3*generator], variableClauses[3*generator+1], variableClauses[3*generator+2])) 


def generateRandomString():
    randomString = [0]*temporalClause[0]
    stringGenerated = ''
    for i in range(0,20):
        randomString[i] = random.randint(0, 1)
        stringGenerated += str(randomString[i])
    return stringGenerated, randomString  

def arrayToString(initialArray):
    stringGenerated = ''
    for elements in initialArray: 
        stringGenerated+= str(elements)
    return stringGenerated

'''
    All clauses are checked and depending on it's value, we append them into an array, if any of the
    3 variables in the clause is lower than 0 it means it's a negative clause so we just flip the
    original value. As we have an OR, a clause is satisfied when at least one of the variables is 
    a 1, a clause is unsatisfied if all 3 variables are 0. If all clauses are satisfied then we
    stop the program as there is nothing left to do but if there are unsatisfied clauses, one of
    these is chosen randomly along with one of the variables that make up the clause and the value 
    is flipped so we can repeat it 20 times. 
'''

initialString,initialStringArray, = generateRandomString()
satisfiedClauses = []
unsatisfiedClauses = []
steps = []
checkClause = []
f = open("output.txt", "w")


for repetitions in range(0,60):
    f.write("Iteration: "+str(repetitions+1) +'\n')
    satisfiedClauses = []
    unsatisfiedClauses = []
    for clause in allClauses:
        checkClause = []
        if(clause[0]<0):
            if(initialStringArray[abs(clause[0])-1]=="0"):
                checkClause.append(1)
            else:
                checkClause.append(0)
        else: checkClause.append(int(initialStringArray[abs(clause[0])-1]))
        if(clause[1]<0):
            if(initialStringArray[abs(clause[1])-1]== "0"):
                checkClause.append(1)
            else:
                checkClause.append(0)
        else: checkClause.append(int(initialStringArray[abs(clause[1])-1]))
        if(clause[2]<0):
            if(initialStringArray[abs(clause[2])-1]=="0"):
                checkClause.append(1)
            else:
                checkClause.append(0)
        else: checkClause.append(int(initialStringArray[abs(clause[2])-1]))      
        if(any(checkClause)):
            satisfiedClauses.append((checkClause,clause))
        else:
            unsatisfiedClauses.append((checkClause,clause))
    f.write("Binary string tested: "+initialString +'\n')
    f.write("Satisfied clauses: "+str(len(satisfiedClauses)) +'\n')
    f.write("Unsatisfied clauses: "+str(len(unsatisfiedClauses))+'\n')
    if(len(satisfiedClauses)==91):
        break
    else:
        clauseToChange = random.randint(0, len(unsatisfiedClauses)-1)
        variableToChange = random.randint(0,2)
        if( initialStringArray [abs(int(unsatisfiedClauses[clauseToChange][1][variableToChange]))-1] == 0 ):
            initialStringArray [abs(int(unsatisfiedClauses[clauseToChange][1][variableToChange]))-1] =1
            
        else:
            initialStringArray [abs(int(unsatisfiedClauses[clauseToChange][1][variableToChange]))-1] = 0
        steps.append(len(unsatisfiedClauses)) 

    f.write("Chosen clause: ("+ str(unsatisfiedClauses[clauseToChange][1][0])+" "+str(unsatisfiedClauses[clauseToChange][1][1])+" "+str(unsatisfiedClauses[clauseToChange][1][2])+" "+")"+'\n')
    f.write("Chosen varible: "+ str(unsatisfiedClauses[clauseToChange][1][variableToChange])+'\n')
    f.write("New string to be tested: "+ arrayToString(initialStringArray) +'\n\n')
    
f.close()
'''
    Finally we make a graph, consisting on all the steps the unsatisfied clauses make on every
    iteration so we can see the changes. This graph is stored on the same folder where all 
    other files needed for the project are saved. 
'''
plt.figure(figsize=(15, 10))
plt.plot(steps, 'm', marker=".", markersize=10, linestyle='None', label='')
for iteration in range(0,60):
    plt.annotate(str(steps[iteration]), (iteration, steps[iteration]+0.2))
plt.xticks(range(0,60), rotation=70, fontsize=8)
plt.xlabel('Iterations')
plt.ylabel('Unsatisfied Clauses')
plt.savefig('jumps.png')

print("You can find the results in output.txt and jumps.png respectively")
