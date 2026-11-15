import random

class AnimalFarmCFG:
    def __init__(self):
        self.non_terminals = [ 'P', 'S1', 'S2',
            'EventNP', 'PassiveTaken', 'TimeAdv',
            'PassiveConsensus', 'AgentPP', 'SubjPlural', 'PredPlural',
            'MatchedDissenters', 'DissentRole', 'GroupAnimal', 'SingAnimal',
            'SeqAdv', 'PassiveDiscovery', 'IronyVP' ]

        self.rules = {
            # Paragraph structure mirroring the two-sentence Orwellian passage
            'P': [
                ['S1', 'S2']
            ],

            # Sentence 1: Compound passive motion + consensus complement clause
            'S1': [
                [
                    'EventNP', 'PassiveTaken', 'TimeAdv', ',', 'and',
                    'PassiveConsensus', 'AgentPP', 'that',
                    'SubjPlural', 'were', 'PredPlural', '.'
                ]
            ],

            # Sentence 2: Existential count + appositive split + ironic relative clause
            'S2': [
                [
                    'there were', 'MatchedDissenters', ',',
                    'who was', 'SeqAdv', 'PassiveDiscovery', 'IronyVP', '.'
                ]
            ],

            # Sentence 1 Constituents
            'EventNP': [
                ['the vote'], ['the resolution'], ['the motion'],
                ['the question'], ['the proposal']
            ],
            'PassiveTaken': [
                ['was taken'], ['was put'], ['was passed'], ['was settled']
            ],
            'TimeAdv': [
                ['at once'], ['without delay'],
                ['before the assembly'], ['in the big barn']
            ],
            'PassiveConsensus': [
                ['it was agreed'], ['it was decided'],
                ['it was resolved'], ['it was declared']
            ],
            'AgentPP': [
                ['by an overwhelming majority'],
                ['by a unanimous show of hooves'],
                ['by nearly all present'],
                ['with loud acclamation']
            ],
            'SubjPlural': [
                ['rats'], ['wild creatures'], ['rabbits'],
                ['pigeons'], ['all four-legged animals']
            ],
            'PredPlural': [
                ['comrades'], ['friends'], ['allies'], ['equals'], ['brothers']
            ],

            # Sentence 2 Constituents (Context-free paired counts & singular attachment)
            'MatchedDissenters': [
                ['only four', 'DissentRole', ',', 'the three', 'GroupAnimal', 'and', 'SingAnimal'],
                ['only five', 'DissentRole', ',', 'the four', 'GroupAnimal', 'and', 'SingAnimal'],
                ['only three', 'DissentRole', ',', 'the two', 'GroupAnimal', 'and', 'SingAnimal']
            ],
            'DissentRole': [
                ['dissentients'], ['objectors'], ['doubters'], ['opponents']
            ],
            'GroupAnimal': [
                ['dogs'], ['hens'], ['sheep'], ['pigs']
            ],
            'SingAnimal': [
                ['the cat'], ['the raven'], ['the donkey'], ['the goat']
            ],
            'SeqAdv': [
                ['afterwards'], ['later'], ['subsequently'], ['shortly after']
            ],
            'PassiveDiscovery': [
                ['discovered to have'], ['found to have'],
                ['observed to have'], ['suspected to have']
            ],
            'IronyVP': [
                ['voted on both sides'],
                ['slept through the entire debate'],
                ['abstained from both counts'],
                ['slipped away before the final tally'],
                ['nodded in agreement with every speaker']
            ]
        }

    def expand(self, symbol):
        """Recursively expands a non-terminal symbol into terminal tokens."""
        if symbol not in self.rules:
            return [symbol]
        production = random.choice(self.rules[symbol])
        tokens = []
        for sym in production:
            tokens.extend(self.expand(sym))
        return tokens

    def generate_paragraph(self):
        """Generates a punctuated, capitalized paragraph from start symbol P."""
        tokens = self.expand('P')
        text = ' '.join(tokens)
        text = text.replace(' ,', ',').replace(' .', '.')
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        return '. '.join(s[0].upper() + s[1:] for s in sentences) + '.'


if __name__ == "__main__":
    cfg = AnimalFarmCFG()
    for i in range(3):
        print(f"Sample {i+1}:\n{cfg.generate_paragraph()}\n")
