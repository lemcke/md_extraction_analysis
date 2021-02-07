from matscipy.neighbours import neighbour_list

def find_bonds(atoms, cutoffs_dict):
    """Returns a set of (frozen)sets of indices,
    where each set represents a bond, and the two
    values in the set represent the indices of the
    atoms in the system.

    ARGUMENTS
    ---------
    atoms        :    <ase.atoms.Atoms> object
    cutoffs_dict :    <dict> of cutoffs with the form
                        { (species tuple) : cutoff }

                      Example:
                      --------  
                        cutoffs_dict = {
                            ('C', 'C') : 1.8,
                            ('C', 'H') : 1.3,
                            ('H', 'H') : 0.9
                        }

    COMMENTS
    --------
    - Matscipy is used to generate the neighbour lists,
    which are determined by simple cutoffs. The function
    assumes that two atoms form a `bond' if they are within
    the cutoff length corresponding to that bond type.

    - By returning a `set', it is ensured that there are
    no redundant bonds, since {a, b} == {b, a}.

    - This function can also be used to find bond events by
    comparing the bond sets from consecutive simulation
    steps and taking the symmetric difference between the two.
    Note that the order *does* matter!
    
    For example:
    >>> bonds_initial = find_bonds( atoms_initial, cutoffs )
    >>> bonds_final   = find_bonds( atoms_final, cutoffs )
    >>>
    >>> bonds_final - bonds_initial
    {frozenset({74, 29})
     frozenset({104, 19})}
    >>> # two bonds have been created
    >>> 
    >>> bonds_initial - bonds_final
    {frozenset({31, 78})}
    >>> # one bond has been broken
    """
    i,j = neighbour_list('ij', atoms, cutoffs_dict)

    return set( frozenset( {x, y} ) for x, y in zip(i, j) )
