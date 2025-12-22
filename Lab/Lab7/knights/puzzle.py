from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

ASaidKnight = Symbol("A said 'I am a Knight'")
ASaidKnave = Symbol("A said 'I am a Knave'")

def One(knight_sym, knave_sym):
    return And(
        Or(knight_sym, knave_sym),
        Not(And(knight_sym, knave_sym))
    )

statement0 = And(AKnight, AKnave)
knowledge0 = And(
    One(AKnight, AKnave),
    One(BKnight, BKnave),
    One(CKnight, CKnave),
    Implication(AKnight, statement0),
    Implication(AKnave, Not(statement0))
)

statement1 = And(AKnave, BKnave)
knowledge1 = And(
    One(AKnight, AKnave),
    One(BKnight, BKnave),
    One(CKnight, CKnave),
    Implication(AKnight, statement1),
    Implication(AKnave, Not(statement1))
)

same_kind = Or(And(AKnight, BKnight), And(AKnave, BKnave))
different_kind = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    One(AKnight, AKnave),
    One(BKnight, BKnave),
    One(CKnight, CKnave),
    Implication(AKnight, same_kind),
    Implication(AKnave, Not(same_kind)),
    Implication(BKnight, different_kind),
    Implication(BKnave, Not(different_kind))
)

knowledge3 = And(
    One(AKnight, AKnave),
    One(BKnight, BKnave),
    One(CKnight, CKnave),
    And(
        Or(ASaidKnight, ASaidKnave),
        Not(And(ASaidKnight, ASaidKnave))
    ),
    Implication(AKnight,
                And(
                    Implication(ASaidKnight, AKnight),
                    Implication(ASaidKnave, AKnave)
                )),
    Implication(AKnave,
                And(
                    Implication(ASaidKnight, Not(AKnight)),
                    Implication(ASaidKnave, Not(AKnave))
                )),
    Implication(BKnight, ASaidKnave),
    Implication(BKnave, Not(ASaidKnave)),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
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
