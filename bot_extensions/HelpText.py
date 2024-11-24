roll_long="""A roll is an arithmetic expression that may include dice rolls. You can include variables inside of the expression as well, which refer to other saved rolls. For example:

    !roll a=1d8
    !roll b=a + 7
    !roll b --> 1d8 + 7 --> b: 7 + 7 = 14

!roll stealth
    If there is a roll called "stealth", then this command will roll the dice and resolve the expression

!roll stealth = 1d20 + dex + expert
    This will create or overwrite a roll called "stealth"

!roll list <page>
    Returns a list of rolls. If there are multiple pages, you can add an optional page argument to see a different page. ` indicates a roll is a composite. Counters appear as "total / max".

!roll search stealth
    Returns a search for a roll called "stealth"

!roll delete stealth
    Deletes the roll called "stealth"
"""

composite_long="""A composite is a \"roll\" that is made by adding multiple rolls together. You can roll a composite using the "roll" command like you would any other roll. For example, the following composite would be rolled as "1d20 + dex + prof".

    {
        base: 1d20,
        modifier: dex,
        proficiency: prof
    }

!composite acrobatics 
    See the rolls that make up the composite

!composite acrobatics proficiency=expert
    Create/modify a roll within the "acrobatics" composite

!composite create acrobatics base=1d20 modifier=dex proficiency=prof
    Create a new composite called "acrobatics"

!composite search acrobatics
    Search your character for a composite called "acrobatics"

!composite delete acrobatics
    Delete a composite called "acrobatics"

!composite acrobatics remove proficiency
    Remove the roll labeld "proficiency" from the "acrobatics" composite
"""

counter_long="""A counter has a total, a max value, and a min value. The total can never go above the max or below the min.

    {
        total: 10,
        max: 10,
        min: 0
    }

!counter create hitpoints
    Creates a new counter called "hitpoints". The default max is 10, and the default min is 0. The total will start at the max.

!counter create hitpoints max=100 total=8
    Creates a new counter with a specified max and current total

!counter hitpoints max
    Set the hitpoint counter total to the maximum value

!counter hitpoints min
    Set the hitpoint coutner total to the minimum value

!counter hitpoints total=20
    Set the hitpoint counter total to 20.

!counter hitpoints +8
    Increase the counter total by 8

!counter hitpoints -8
    Reduce the counter total by 8

!counter list <page>
    Returns a list of counters. If there are multiple pages, you can add an optional page argument to see a different page.

!counter search hitpoints
    Returns a search for a counter called hitpoints

!counter delete hitpoints
    Attempts to delete a counter called hitpoints
"""

func_long="""Create, modify, delete functions capable of executing commands

!func create dagger | roll dagger_hit; roll dagger_dmg
    Creates a function that executes two different roll commands

!func create cast $slot | counter $slot -1; roll spell_hit; roll spell_save;
    Creates a function that takes an argument

!func cast first
    Executes the "cast" function with an argument present for the counter command.

!func list <page>
    Returns a list of funcs. If there are multiple pages, you can add an optional page argument to see a different page.

!func delete dagger
    Deletes a function called dagger
"""