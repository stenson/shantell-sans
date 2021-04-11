"""
    Uses FontTools buildStatTable to add a defined STAT table to a variable font
"""

from fontTools.otlLib.builder import buildStatTable, _addName
from fontTools.ttLib import TTFont
import sys


AXES = [
    dict(
        tag="wght",
        name="Weight",
        ordering=0,
        values=[
            dict(nominalValue=300, rangeMinValue=300, rangeMaxValue=350, name="Light"),
            dict(nominalValue=400, rangeMinValue=350.00001, rangeMaxValue=450, name="Regular", flags=0x2, linkedValue=700),
            dict(nominalValue=500, rangeMinValue=450.00001, rangeMaxValue=550, name="Medium"),
            dict(nominalValue=600, rangeMinValue=550.00001, rangeMaxValue=650, name="SemiBold"),
            dict(nominalValue=700, rangeMinValue=650.00001, rangeMaxValue=750, name="Bold"),
            dict(nominalValue=800, rangeMinValue=750.00001, rangeMaxValue=850, name="ExtraBold"),
        ],
    ),
    dict(
        tag="BNCE",
        name="Bounce",
        ordering=1,
        values=[
            dict(nominalValue=0, rangeMinValue=0, rangeMaxValue=0, name="No Bounce", flags=0x2),
            dict(nominalValue=50, rangeMinValue=0.00001, rangeMaxValue=75,  name="SemiBouncy"),
            dict(nominalValue=100, rangeMinValue=75.00001, rangeMaxValue=100,  name="Bouncy"),
        ],
    ),
    dict(
        tag="IRGL",
        name="Irregularity",
        ordering=2,
        values=[
            dict(nominalValue=0, rangeMinValue=0, rangeMaxValue=25, name="Normalized", flags=0x2),
            dict(nominalValue=100, rangeMinValue=25.00001, rangeMaxValue=100,  name="Irregular"),
        ],
    ),
]

## adds 
def update_fvar(ttfont):
    fvar = ttfont['fvar']
    nametable = ttfont['name']
    family_name = nametable.getName(16, 3, 1, 1033) or nametable.getName(1, 3, 1, 1033)
    family_name = family_name.toUnicode().replace(" ", "")
    nametable.setName(family_name, 25, 3, 1, 1033)
    for instance in fvar.instances:
        instance_style = nametable.getName(instance.subfamilyNameID, 3, 1, 1033).toUnicode()
        ps_name = f"{family_name}-{instance_style.replace(' ', '')}"
        instance.postscriptNameID = _addName(nametable, ps_name, 256)


def main():
    filepath = sys.argv[1]
    tt = TTFont(filepath)

    buildStatTable(tt, AXES)
    update_fvar(tt)
    tt.save(filepath)
    print(f"Added STAT table to {filepath}")


if __name__ == "__main__":
    main()