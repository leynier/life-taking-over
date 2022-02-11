from compGlobals import TokeTypes 


production = {
    "D": [
        [TokeTypes.tokBool, TokeTypes.tokID, TokeTypes.tokAssign, "E"],
        [TokeTypes.tokInt, TokeTypes.tokID, TokeTypes.tokAssign, "E"],
        [TokeTypes.tokString, TokeTypes.tokID, TokeTypes.tokAssign, "E"],
        [TokeTypes.tokDouble, TokeTypes.tokID, TokeTypes.tokAssign, "E"],
    ],
    "E": [["V", "S"]],
    "V": [["P", "M"]],
    "P": [["B"], [TokeTypes.tokOpenParen, "E", TokeTypes.tokClosedParen]],
    "B": [
        [TokeTypes.tokString],
        [TokeTypes.tokInt],
        [TokeTypes.tokDouble],
        [TokeTypes.tokTrue],
        [TokeTypes.tokFalse],
        [TokeTypes.tokID],
    ],
    "M": [
        ["empty"],
        [TokeTypes.tokMul, "P", "Y"],
        [TokeTypes.tokDiv, "P", "Y"],
        [TokeTypes.tokModDiv, "P", "Y"],
        [TokeTypes.tokPow, "P", "Y"],
    ],
    "S": [
        ["empty"],
        [TokeTypes.tokSum, "V", "S"],
        [TokeTypes.tokSub, "V", "S"],
    ],
    "L": [[TokeTypes.tokLoop, TokeTypes.tokOpenBracket]],
    "K": [
        [
            TokeTypes.tokIf,
            TokeTypes.tokOpenParen,
            "X",
            TokeTypes.tokClosedParen,
            TokeTypes.tokOpenBracket,
        ]
    ],
    "X": [["E", "O"]],
    "O": [["empty"], ["C", "E", "N"]],
    "C": [
        [TokeTypes.tokGreaterOrEqual],
        [TokeTypes.tokLessOrEqual],
        [TokeTypes.tokNotEqual],
        [TokeTypes.tokEqual],
        [TokeTypes.tokGreater],
        [TokeTypes.tokLess],
    ],
    "N": [["empty"], [TokeTypes.tokOr, "X"], [TokeTypes.tokAnd, "X"]],
}
