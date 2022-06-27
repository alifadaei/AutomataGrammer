from tracemalloc import start


class Grammer:
    def __init__(self, rules) -> None:
        self.rules = rules


class FormalGrammer(Grammer):
    def __init__(self, rules) -> None:
        super().__init__(rules)
        self.isFormal = self.checkFormal()

    def isLinear(self, string):
        grammerType = False
        if string.islower():
            return True
        firstLetter = string[0]
        lastLetter = string[-1]
        if firstLetter.isupper():  # must be left linear grammer
            grammerType = 'left'
            if not string[1:].islower():  # it is not linear!
                return False
        elif lastLetter.isupper():  # must be right linear grammer
            grammerType = 'right'
            if not string[:-1].islower():  # it is not linear!
                return False
        return grammerType

    def checkFormal(self):
        # filter the A->abcd formats
        reducedRules = list(
            filter(lambda rule: not rule[1].islower(), self.rules))
        gtype = self.isLinear(reducedRules[0][1])
        for rule in reducedRules:
            ruleType = self.isLinear(rule[1])
            if (not len(rule[0]) == 1) or (not ruleType) or (ruleType != gtype):
                return False
        return gtype

    def getMachine(self):
        if(not self.isFormal):
            return None
        transitions = []
        for rule in self.rules:
            if rule[1].islower():
                transition = (rule[0], rule[1], 'F')
            elif self.isFormal == 'right':  # right linear grammer
                transition = (rule[0], rule[1][:-1], rule[1][-1])
            else:  # left linear grammer
                transition = (rule[0], rule[1][1:], rule[1][0])
            transitions.append(transition)
        machine = FiniteMachine(transitions)
        return machine


class FiniteMachine:
    def __init__(self, transitions) -> None:
        self.transitions = transitions
        states = {'F'}
        characters = set
        for transition in self.transitions:
            states.add(transition[0])
            characters = characters.union(set(list(transition[1].split(' '))))
        self.states = states
        self.characters = characters

    def printMachine(self):
        print("Starting state(q0): ", 'S')
        print('states(Q): ', self.states)
        printTransitions = []
        for trans in self.transitions:
            suitableTrans = f'δ({trans[0]}, {trans[1]}) => {trans[2]}'
            printTransitions.append(suitableTrans)
        print('transitions(T): ', printTransitions)
        print('AllowedCharacters(Σ): ', self.characters)
        print('FinalState: ', 'F')

    def accepts(self, string, startIndex, initialState):
        if(initialState == 'F'):
            return True
        possibleTransitions = list(
            filter(lambda trans: trans[0] == initialState, self.transitions))
        for trans in possibleTransitions:
            # if the transition fits in current state and couuld be applied
            word = trans[1]  # the transition string
            nextIndex = startIndex + len(word)
            if string[startIndex:nextIndex] == word:
                if self.accepts(string, nextIndex, trans[2]):
                    return True
        return False


f = FormalGrammer(
    [('B', 'aB'), ('S', 'aB'), ('B', 'b')])
machine = f.getMachine()
machine.printMachine()
print(machine.accepts('assab', 0, 'S'))
