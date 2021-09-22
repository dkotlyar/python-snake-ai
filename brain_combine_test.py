from brain import Brain

brain1 = Brain()
brain2 = Brain()

child = Brain.combine(brain1, brain2)

print(child, child.layers)