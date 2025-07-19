1. water
> Key Mechanics

# Banked
Banked Moves are stored in the Bank, a set of Non-Active Moves.
Banked Moves cannot be used directly, but can be referenced by other moves.
Moves lose Counters like Cooldown/Charge when switching zones (active/banked)

Moves:
    - Bank Moves / Unbank Moves
    - Reference Banked Move Total/Elements on Self
    - 

Blessings:
    - Expand number of Bank Slots
    - Allow Players to Move Banked or Unbanked Moves in Game

> Secondary Mechanics

# Attunements


# Statuses

# Declaration
    - Nullify Declarations


2. stone
> Key Mechanics

# Cooldown
Prevents Actions from being used for set number of turns.
Reduces by 1 at end of each turn.
Moves with Cooldown lose Cooldown when Changing Zones (Active / Banked)

Moves:
    - Ignore / Reduce Self Cooldown
    - Reference Moves on Cooldown Total/Turns on Cooldown
    - Apply Cooldown to Enemy Moves

Blessings:
    - Moves with Cooldown + 1 Iters

# Iters
Iters is how many times attacks are executed in a turn during combat.
Players default to Iters 1, but moves have iters modifiers which are local or fall onto future moves.
Some Utility Moves are 'Iterable', but almost none are.

> Secondary Mechanics

# Banked
Moves:
    - Bank Self as Cost
    - Abilities from Bank
    - If Banked: Start of Turn Gain +1 Tough
    - While Banked, If Move Gains Cooldown, trigger and ignore (cooldown 3)
    - Deals X Damage. X = 1. While Banked: X += 1. (Cooldown 2)

3. fire
> Key Mechanics

# Burn
Burn Deals 1 Fire Damage to Players at the start of their turn.
If a Player at the burn ceiling has a Burn Applied to them, they 'Burn-Out'. 
The Default Burn-Ceiling is 3.

Moves:
    - Apply Burn Enemy
    - Reference Self Burn Total
    - Apply Burn to Self as a Risk-Punishment

Blessings:
    - When Burnt, Moves on 'Cooldown' Lose Cooldown
    - When Applying Burn, Apply 1 More (total) (Cooldown 1)

# Anger
Anger is a Move-Restricting Ability which Prevents Utility Moves.
Players with Anger can attempt to use utility moves, but are warned.
If Applied Post-Choice, Pre-Execution, their Move is Skipped.

Moves:
    - Apply Anger as Risk-Punishment
    - Apply Anger to Self as Cost

Blessing:
    - While Self-Anger Deal & Take Extra Damage
    - While Self-Anger Ignore Sleep / Stun

# Burn-Out
Player Takes Damage Equal to their Burn Total and Loses all Burns.
Additionally, Burnt-Out Players gain 1 'Anger' upon being Burnt-Out.

Blessings:
    - When Player is Burnt-Out, They lose all but 1 Burn

# Declaration

Moves:
    - Reference Declarations Total/Active/Successful
    - Make Private Declarations with Delayed Effects
    - 

Blessings:
    - When Declaration Comes True: Apply 1 Burn to Target

4. plant
> Key Mechanics

# Regen


# Bound


# Sleep


> Secondary Mechanics

# Banked
    - Abilities from Bank
    - If Banked: Start of turn Increase 1 Variable on chosen move by 1 for this turn.
    - When Banked: All Players Gain 1 Sleep
    - If Banked: Start of turn Gain 1 Regen.

# Declaration




5. vital
> Self-Status

6. force

7. thunder
> Key Mechanics

# Charge
Charge is an amount of 'stored energy' on a move that downticks at the end of each turn.
Moves with 'Charge' have additional effects that only work while charged.
A move with charge will either re-charge itself (restore charge up to initial value) or Discharge itself.
Discharged Moves are still playable.

Moves:
    - Moves with If-Charged: Abilities
    - Discharge/Recharge Triggers
    - Reference to Charge Totals
    - Spend Charge from Other Moves

Blessings:
    - Blessings with Charge
    - If a move is discharged: Recharge it (Charge 2)
    - At Start of Turn: Self Iters += 1 (Charge 1)

> Secondary Mechanics

# Quick
Quick is a Turn-Order Modifying Status.
Players with Quick get +1 Speed during turn-order calculation.

Moves:
    - Applies Quick to self if charged
    - Deals More Damage if Quick
    - Self.Quick.Turns += X. X=Charge (Charge 2)

Blessings:
    - Whenever Move is Discharged: Gain 1 Quick

# Quick-Moves
Quick-Moves are Moves which have a Speed Modifier Applied to them.
Players using Quick-Moves will gain an additional 1 speed during that turn.
Quick-Moves stack with Quick, which together interoperate with Slow and Slow-Moves.

Moves:
    - Deals 2 Damage. If Charged: Quick-Move

Blessings:
    - Quick Moves 

# Stun
Stun is a Move-Preventing Status which prevents the use of Attacks.
Like Anger, Players 'can' attempt attacks while stunned, but will be warned.
If Applied Post-Choice, Pre-Execution, their Move is Skipped.

Moves:
    - Recharge a Move. If > 4 Charge is applied this way, Target Becomes Stunned
    - 

Blessings:
    - 

# Retaliate
Retaliation Effects Take Place when a player has Damage Dealt to them
