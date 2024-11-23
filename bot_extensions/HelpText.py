roll_long="""A roll is an arithmetic expression that may include dice rolls. You can include variables inside of the expression as well, which refer to other saved rolls. For example:

    !roll a=1d8
    !roll b=a + 7
    !roll b --> 1d8 + 7 --> b: 7 + 7 = 14

!roll stealth
    If there is a roll called "stealth", then this command will roll the dice and resolve the expression

!roll stealth = 1d20 + dex + expert
    This will create or overwrite a roll called "stealth"

!roll list <page>
    Returns a list of rolls. If there are multiple pages, you can add an optional page argument to see a different page.

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