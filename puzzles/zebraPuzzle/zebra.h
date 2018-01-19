#ifndef ZebraPuzzle_Header
#define ZebraPuzzle_Header

// AssignRow macro used by ZebraPuzzle to make row index
// pointer assignments less repetitive to code.
#define AssignRow(array, one, two, three, four, five) { \
    one   = &array[0],                                  \
    two   = &array[1],                                  \
    three = &array[2],                                  \
    four  = &array[3],                                  \
    five  = &array[4];                                  \
}                                                       \

/**
 * ZebraPuzzle:
 * stores the possible states of dictated by the
 * conditions of the puzzle whilst implementing methods to sovlve it.
 * Its only public method other than its initialiser is `solve`.
*/
class ZebraPuzzle {

    int orderings[5] = {1, 2, 3, 4, 5},
        first = 1, middle = 3, end = 5;

    int colors[5],  *red, *green, *ivory, *yellow, *blue,
        nations[5], *Englishman, *Spaniard, *Ukrainian, *Japanese, *Norwegian,
        drinks[5],  *coffee, *tea, *milk, *oJuice, *WATER,
        smokes[5],  *OldGold, *Kools, *Chesterfields, *LuckyStrike, *Parliaments,
        animals[5], *dog, *snails, *fox, *horse, *ZEBRA;

    bool checkNations(), checkDrinks(), checkSmokes(), checkAnimals();

    // small helper functions for the solve method.
    bool isRight(int a, int b) { return a - b == 1; }
    bool nextTo(int a, int b)  { return abs(a-b) == 1; }

public:
    ZebraPuzzle() {
        AssignRow(colors,  red, green, ivory, yellow, blue);
        AssignRow(nations, Englishman, Spaniard, Ukrainian, Japanese, Norwegian);
        AssignRow(drinks,  coffee, tea, milk, oJuice, WATER);
        AssignRow(smokes,  OldGold, Kools, Chesterfields, LuckyStrike, Parliaments);
        AssignRow(animals, dog, snails, fox, horse, ZEBRA);
    }
    void solve();
};

#endif