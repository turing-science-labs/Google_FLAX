import random
from collections import deque

class ContextSensitiveGrammar:
    def __init__(self, terminals=None, non_terminals=None, start_symbol='S'):
        # Use the curation of robust Animal Farm terminals as default
        self.terminals = terminals if terminals is not None else [
            "All", "animals", "are", "equal", "but", "some", "more", "than", "others",
            "Four", "legs", "good", "two", "bad", "better", "Napoleon", "is", "always",
            "right", "Snowball", "was", "a", "traitor", "No", "animal", "shall", "sleep",
            "in", "bed", "with", "sheets", "drink", "alcohol", "to", "excess", "kill",
            "any", "other", "without", "cause", "Squealer", "says", ".", ",",
            "The", "pigs", "declared", "that", "all", "humans", "are", "enemies",
            "Boxer", "the", "horse", "worked", "harder", "at", "the", "windmill",
            "Benjamin", "donkey", "remained", "silent", "and", "cynical",
            "on", "the", "farm", "in", "the", "barn" ]
        self.non_terminals = non_terminals if non_terminals is not None else [
            "S", "SentenceBody", "Slogan", "Commandment", "Declaration",
            "ContextEqualizer", "LegsSlogan", "LegQualifier", "NapoleonTruth", "ModifiedCommand",
            "Narrative", "Character", "Action", "Location" ]
        self.start_symbol = start_symbol
        # Compacted rules initialization minimizing line count and extra whitespace
        self.rules = {
            ((), "S", ()): [["SentenceBody"]],
            ((), "SentenceBody", ()): [["Slogan"], ["Commandment"], ["Declaration"], ["Narrative"]],
            ((), "Slogan", ()): [["LegsSlogan"], ["NapoleonTruth"]],
            ((), "NapoleonTruth", ()): [["Napoleon", "is", "always", "right", "."], ["Squealer", "says", "Napoleon", "is", "always", "right", "."]],
            ((), "LegsSlogan", ()): [["Four", "legs", "good", ",", "two", "legs", "LegQualifier", "."]],
            ((), "LegQualifier", ()): [["bad"]],
            (("two", "legs"), "LegQualifier", ()): [["better"]],
            ((), "Declaration", ()): [["All", "animals", "are", "equal", "ContextEqualizer", "."]],
            ((), "ContextEqualizer", ()): [[]],
            (("equal",), "ContextEqualizer", ()): [["but", "some", "animals", "are", "more", "equal", "than", "others"]],
            ((), "Commandment", ()): [["No", "animal", "shall", "ModifiedCommand", "."]],
            ((), "ModifiedCommand", ()): [["sleep", "in", "bed"], ["drink", "alcohol"], ["kill", "any", "other", "animal"]],
            (("sleep", "in", "bed"), "ModifiedCommand", ()): [["with", "sheets"]],
            (("drink", "alcohol"), "ModifiedCommand", ()): [["to", "excess"]],
            (("kill", "any", "other", "animal"), "ModifiedCommand", ()): [["without", "cause"]],
            ((), "Narrative", ()): [["Character", "Action", "Location", "."]],
            ((), "Character", ()): [["Boxer"], ["Napoleon"], ["Snowball"], ["Benjamin"], ["Squealer"]],
            ((), "Action", ()): [["worked", "harder"], ["declared", "that", "all", "humans", "are", "enemies"], ["remained", "silent", "and", "cynical"], ["was", "declared", "a", "traitor"]],
            ((), "Location", ()): [["at", "the", "windmill"], ["on", "the", "farm"], ["in", "the", "barn"]]        }

    def display_rules(self, max_display=40):
        print(f"Total unique rules defined: {len(self.rules)}")
        print(f"\n--- Sample of active rules (showing up to {max_display}) ---")
        count = 0
        for (left, nt, right), replacements in self.rules.items():
            if count >= max_display:
                print("... and more rules")
                break
            left_str = " ".join(left) if left else "_"
            right_str = " ".join(right) if right else "_"
            for rep in replacements:
                rep_str = " ".join(rep)
                print(f"Context: [{left_str}] <{nt}> [{right_str}]  ->  {rep_str}")
                count += 1

def generate_all_sentences(csg):
    all_terminal_sentences = set()
    queue = deque([ (csg.start_symbol,) ])
    visited_states = set()
    while queue:
        current_sent = queue.popleft()
        if all(sym in csg.terminals for sym in current_sent):
            all_terminal_sentences.add(" ".join(current_sent))
            continue
        for i in range(len(current_sent)):
            if current_sent[i] in csg.terminals:
                continue
            for (left, nt, right), replacements in csg.rules.items():
                if current_sent[i] == nt:
                    left_len = len(left)
                    right_len = len(right)
                    if left_len > 0:
                        if i < left_len or current_sent[i-left_len:i] != left:
                            continue
                    if right_len > 0:
                        if i + 1 + right_len > len(current_sent) or current_sent[i+1:i+1+right_len] != right:
                            continue
                    for rep in replacements:
                        new_sent = current_sent[:i] + tuple(rep) + current_sent[i+1:]
                        if new_sent not in visited_states:
                            visited_states.add(new_sent)
                            queue.append(new_sent)
    return sorted(list(all_terminal_sentences))

# Initialize the packaged CSG and generate all
csg = ContextSensitiveGrammar()
csg.display_rules(max_display=40)
all_sentences = generate_all_sentences(csg)
print(f"\nTotal possible unique sentences: {len(all_sentences)}")
print("\n--- Every Single Generated Sentence ---")
for idx, sentence in enumerate(all_sentences):
    print(f"{idx + 1:3d}: {sentence}")
