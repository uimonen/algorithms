from dataclasses import dataclass
# Local imports
import state
from action import Action

# This is a dataclass, we want __eq__, __hash__, and __repr__ created
# automatically.
@dataclass(eq=True, unsafe_hash=True, repr=True)
class KnightsState(state.State):
    """
    Describes a 8x8 square board, occupied by 0 - 64 identical 'knight' game
    pieces.

    Each board configuration is a state, and an action consists of moving one
    game piece.

    The game state is described by the occupied board locations. A new state
    is derived by moving one piece to an unoccupied location in accordance with
    a chess knight move.
    """

    # Attributes for dataclass.
    occupied : frozenset

    def __init__(self,occupied):
        """
        Creates a new KnightsState object with pieces at specified locations.


        Parameters
        ----------
        occupied : iterable (e.g. list) of pairs of int in [0,7]
           Describes the occupied locations. E.g `occupied = [(3,2)]` denotes
           a board with a single piece at location (3,2).

        Throws
        ------
        TypeError
           If occupied is on wrong format.
        ValueError
           If board locations are outside.
        """
        # Check that the input is valid.
        for x in occupied:
            if tuple != type(x) or len(x) != 2 \
               or int != type(x[0]) or int != type(x[1]):
                raise TypeError("Occupied locations need to be pairs (tuples of length 2) of int.")
            r,c = x
            if r < 0 or r > 7 or c < 0 or c > 7:
                raise ValueError("Occupied locations need to be within board range [0,7] x [0,7].")
        # All good.
        self.occupied = frozenset(occupied)

    def __str__(self):
        """
        Produces a multi-line string representation of the board state.

        Returns
        -------
        str
           '.' for empty cells, 'K' for occupied.
        """
        # Use . for empty cells, and 'K' for occupied. Newline for every row.
        return "\n".join("".join('K' if (r,c) in self.occupied else '.' \
                                 for c in range(8))\
                         for r in range(8))

    def successors(self):
        """
        Gives all legal moves in the current board configuration in the form of
        actions and new states (the successor board configurations).

        A legal action means that:
           - Only one occupied location changes between this KnightState and
             each successor.
           - The target piece moves into an unoccupied space.
           - The target piece moves within the game board (8x8).
           - Only chess knight moves are considered
             (2 horizontal + 1 vertical, or 1 horizontal + 2 vertical).

        Returns
        -------
        list of (Action,KnightsState) pairs.
           List of all applicable actions and the resulting states.
        """
        # TASK
        # Implement the successors function such that it returns a list of new
        # Action and KnightsState object describing all possible
        # combinations of board states reachable by moving one piece.
        #
        # Algorithm:
        # ---------
        # Let succ be an empty list.
        # For every occupied location (r1,c1) in the current board
        #   For every possible target location (r2,c2) for the knight at (r1,c1)
        #     if (r2,c2) represents a legal move location, then
        #        Create a new Action object for this move (cost = 1 [constant])
        #        Create a new KnightsState object representing the board
        #          after this action;
        #        Append a pair of (action,state) to the list succ.
        #     end if;
        #   end for;
        # end for;
        # Return succ;
        directions = [(-1,2), (1,2), (-2,1), (2,1), (-1,-2), (1,-2), (-2,-1), (2,-1)]
        states = []
        succ = []
        if not self.occupied:
            # There are no successor states on a empty board.
            return []
        elif len(self.occupied) == 64:
            # There are no successor states on a full board.
            return []
        else:
            for state in self.occupied:
                # For every occupied location (r1,c1) in the current board
                for move in directions:
                    # For every move contruct target location (r2,c2) for the knight at (r1,c1)
                    target = tuple(map(lambda x, y: x+y, state, move))
                    if target not in self.occupied:
                        # if the target is not in occupied states
                        r,c = target
                        if r >= 0 and r <= 7 and c >= 0 and c <= 7:
                            # if the move is inside the board
                            for state2 in self.occupied:
                                # construct the new positions
                                if state2 != state:
                                    states.append(state2)
                            # create action
                            action = Action(state, target, 1)
                            states.append(target)
                            #create successor states
                            succ.append( (action, KnightsState( states)))
                            states = []
        return succ

if __name__ == "__main__":
    # Create an empty board.
    s1 = KnightsState(occupied = [])
    print(f"This board is empty:\n{s1}\n")
    #succ = s1.successors()
    #print("S1 succ:")
    #print(succ)
    #print("")

    # Create a board with one knight at location (1,2).
    #s2 = KnightsState(occupied = [(1,2)])
    s2 = KnightsState(occupied = [(4,4)])
    print(f"This board has one knight:\n{s2}\n")
    succ = s2.successors()
    print("S2 succ:")
    print(succ)
    print("")

    # Create a board with two knights; (1,2) and (7,7).
    #s3 = KnightsState(occupied  = [ (1,2), (7,7) ])
    s3 = KnightsState([(5,6), (7,7)])
    #s3 = KnightsState(occupied  = [ (1,2), (0, 4) ])

    print(f"This board has two knights:\n{s3}\n")
    print("s3 occupied = ", s3.occupied)
    succ = s3.successors()
    print("S3 succ:")
    print(succ)
    #print("")
