import x

num1 = int(input("Di un numero: "))
num2 = int(input("Di otro numero: "))

Op = input("Que quieres hacer: ")

if Op == "sumar" or Op == "Sumar" or Op == "SUMAR":
    import prueba_file1
elif Op == "restar" or Op == "Restar" or Op == "RESTAR":
    import prueba_file2
else:
    print("Hijoputa")
