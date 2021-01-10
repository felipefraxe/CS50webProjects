from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentencea0 = And(AKnight, AKnave)
knowledge0 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    Biconditional(sentencea0, AKnight)

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentencea1 = And(AKnave, BKnave)
knowledge1 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Biconditional(sentencea1, AKnight),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentencea2 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
sentenceb2 = Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Biconditional(sentencea2, AKnight),
    Biconditional(sentenceb2, BKnight)

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
sentencea3 = Biconditional(AKnight, Not(AKnave))
sentenceb3 = And(Biconditional(AKnave, BKnight), CKnave)
sentencec3 = AKnight
knowledge3 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    Biconditional(AKnight, sentencea3),
    Biconditional(BKnight, sentenceb3),
    Biconditional(CKnight, sentencec3)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()