/*
ZEBRA PUZZLE / Einstein's Puzzle:

1.  There are five houses.
2.  The Englishman lives in the red house.
3.  The Spaniard owns the dog.
4.  Coffee is drunk in the green house.
5.  The Ukrainian drinks tea.
6.  The green house is immediately to the right of the ivory house.
7.  The Old Gold smoker owns snails.
8.  Kools are smoked in the yellow house.
9.  Milk is drunk in the middle house.
10. The Norwegian lives in the first house.
11. The man who smokes Chesterfields lives in the house next to the man with the fox.
12. Kools are smoked in the house next to the house where the horse is kept.
13. The Lucky Strike smoker drinks orange juice.
14. The Japanese smokes Parliaments.
15. The Norwegian lives next to the blue house.

    Q: Now, who drinks water? Who owns the zebra?

#### Possible cases:

    *Houses      | 1         | 2           |  3        |  4           | 5
    ------------------------------------------------------------------------------
    *Color       | Yellow    | Blue        | Red       | Ivory        | Green
    ------------------------------------------------------------------------------
    *Nationality | Norwegian | Ukrainian   | Englishman| Spaniard     | Japanese
    ------------------------------------------------------------------------------
    *Drink       | Water     | Tea Milk    | Orange    | juice        | Coffee
    ------------------------------------------------------------------------------
    *Smoke       | Kools     | Chesterfield| Old Gold  | Lucky Strike | Parliament
    ------------------------------------------------------------------------------
    *Pet         | Fox       | Horse       | Snails    | Dog          | Zebra

#### Notes:

Brute force for all options is 5! per class (120), 5!**5
for each permutation (24.9 billion possible) pc can only
do about 1 billion instructions per sec. will need to use
branching so we dont have to check everything.
*/
#include <iostream>
#include <algorithm>
#include <stdlib.h>
#include "zebra.h"


int main() {
    ZebraPuzzle solver;
    solver.solve();
}

/*
#### Strategy:

Run through the all rules above in-order of highest elimination.
We can use c++'s std::next_permutation to run through the combinations
for each list. Labeling array indexes with human reable names will make
the conditional logic of the program more readable and easier to debug.
Insted of using a large function with nested loops and conditions
break it up into smaller functions that will each introduce a new set of
permutations. Each branching function will return true or false after
checking the conditions it is responsible for. this will return false unless
it traverses through all the functions and all contions are me.
*/

void ZebraPuzzle::solve() {
    std::copy(orderings, orderings+end, colors);
    do {
        // check condition 6 then the rest.
        if (isRight(*green, *ivory) && checkNations()) {
            std::cout << "House " << *WATER << " drinks water, "
                      << "house " << *ZEBRA << " owns the zebra."
                      << std::endl;
            return;
        }
    } while (std::next_permutation(colors, colors+end));
    // Failed search notify user.
    std::cout << "Failed Search." << std::endl;
}

// conditions 2, 10, 15 + checkDrinks
bool ZebraPuzzle::checkNations() {
    std::copy(orderings, orderings+end, nations);
    do {
        if (*Englishman == *red &&        // #2
            *Norwegian == first &&        // #10
            nextTo(*Norwegian, *blue) &&  // #15
            checkDrinks()) {
            return true;
        }
    } while (std::next_permutation(nations, nations+end));
    return false;
}

// checks conditions 4, 5, 9 + checkSmokes
bool ZebraPuzzle::checkDrinks() {
    std::copy(orderings, orderings+end, drinks);
    do {
        if (*coffee == *green &&    // #4
            *Ukrainian == *tea &&   // #5
            *milk == middle &&      // #9
            checkSmokes()) {
            return true;
        }
    } while (std::next_permutation(drinks, drinks+end));
    return false;
}

// checks conditions 8, 13, 14 + checkAnimals
bool ZebraPuzzle::checkSmokes() {
    std::copy(orderings, orderings+end, smokes);
    do {
        if (*Kools == *yellow &&         // #8
            *LuckyStrike == *oJuice &&   // #13
            *Japanese == *Parliaments && // #14
            checkAnimals()) {
            return true;
        }
    } while (std::next_permutation(smokes, smokes+end));
    return false;
}

// checks conditions 3, 7, 11, 12.
bool ZebraPuzzle::checkAnimals() {
    std::copy(orderings, orderings+end, animals);
    do {
        if (*Spaniard == *dog &&             // #3
            *OldGold == *snails &&           // #7
            nextTo(*Chesterfields, *fox) &&  // #11
            nextTo(*Kools, *horse)) {        // #12
            return true;                    // valid combination found.
        }
    } while (std::next_permutation(animals, animals+end));
    return false;
}