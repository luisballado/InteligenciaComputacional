from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.hedges import very
from fuzzylogic.functions import R, S

s1 = Domain("S1", 0, 100)
s2 = Domain("S2", 0, 100)
s3 = Domain("S3", 0, 100)
s4 = Domain("S4", 0, 100)

tiempo = Domain("Tiempo", 0, 60)

tiempo.mucho = R(75,100)
tiempo.mas_menos = R(50,75)
tiempo.poco  = R(25,50)
tiempo.nada  = R(0,25)

s1.muy_lleno  = R(75,100)
s1.lleno      = R(50,75)
s1.semi_lleno = R(25,50)
s1.vacio      = R(0,25)

s2.muy_lleno  = R(75,100)
s2.lleno      = R(50,75)
s2.semi_lleno = R(25,50)
s2.vacio      = R(0,25)

s3.muy_lleno  = R(75,100)
s3.lleno      = R(50,75)
s3.semi_lleno = R(25,50)
s3.vacio      = R(0,25)

s4.muy_lleno  = R(75,100)
s4.lleno      = R(50,75)
s4.semi_lleno = R(25,50)
s4.vacio      = R(0,25)

R1  = Rule({(s1.muy_lleno, s2.muy_lleno, s3.muy_lleno, s4.muy_lleno): tiempo.mucho})
R2  = Rule({(s1.lleno, s2.lleno, s3.lleno, s4.lleno): tiempo.mas_menos})
R3  = Rule({(s1.semi_lleno, s2.semi_lleno, s3.semi_lleno, s4.semi_lleno): tiempo.poco})
R4  = Rule({(s1.vacio, s2.vacio, s3.vacio, s4.vacio): tiempo.nada})

rules = Rule(
    {
        (s1.muy_lleno, s2.muy_lleno, s3.muy_lleno, s4.muy_lleno): tiempo.mucho,
        (s1.lleno, s2.lleno, s3.lleno, s4.lleno): tiempo.mas_menos,
        (s1.semi_lleno, s2.semi_lleno, s3.semi_lleno, s4.semi_lleno): tiempo.poco,
        (s1.vacio, s2.vacio, s3.vacio, s4.vacio): tiempo.nada
    }
)

rules == R1 | R2 | R3 | R4 == sum([R1, R2, R3, R4])

values = {s1: 10, s2: 20, s3: 30, s4: 40}

print(R1(values), R2(values), R3(values), R4(values), "=>", rules(values))
