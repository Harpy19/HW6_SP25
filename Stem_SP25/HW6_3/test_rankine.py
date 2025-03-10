# import
from rankine import rankine
from Steam import steam

"""
This program takes the information from 'rankine' and steam' to compute the efficiency and accuracy of the rankine cycle
for saturated and superheated.
"""

def main():

    rankine1 = rankine(p_low=8, p_high=8000, t_high=None, name='Saturated Rankine Cycle')
    eff1 = rankine1.calc_efficiency()
    print("Cycle 1 Efficiency:", eff1)
    rankine1.print_summary()

    sat_state = steam(8000, x=1, name='Saturated State')
    t1_super = 1.7 * sat_state.T
    rankine2 = rankine(p_low=8, p_high=8000, t_high=t1_super, name='Superheated Rankine Cycle')
    eff2 = rankine2.calc_efficiency()
    print("\nCycle 2 Efficiency:", eff2)
    rankine2.print_summary()

if __name__ == '__main__':
    main()